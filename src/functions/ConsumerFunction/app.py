import json
import boto3
import os
import uuid
from aws_lambda_powertools import Logger, Metrics, Tracer
from aws_lambda_powertools.utilities.typing import LambdaContext

_table_name = os.getenv('TABLE_NAME')
_bucket_name = os.getenv('BUCKET_NAME')

s3 = boto3.resource('s3')
ddb = boto3.resource('dynamodb')
table = ddb.Table(_table_name)

logger = Logger()
tracer = Tracer()
metrics = Metrics()


@metrics.log_metrics(capture_cold_start_metric=True)
@logger.inject_lambda_context
@tracer.capture_lambda_handler
def main(event, context: LambdaContext):
    request_id = context.aws_request_id or uuid.uuid4()
    logger.structure_logs(append=True, requestId=request_id)
    try:
        # read s3 object
        logger.info(f'Consumer lambda called with requestId {request_id}')
        for record in event['Records']:
            message_body = json.loads(record['body'])
            logger.info(f'sqs message body: {message_body}')
            s3object = s3.Object(_bucket_name, message_body['file_name'])
            file_content = s3object.get()['Body'].read().decode('utf-8')
            json_content = json.loads(file_content)
            logger.info(f'json content read from s3 object: {json_content}')

            common_keys = ['groupId', 'region', 'groupName']
            item_keys = ['userId', 'hobby', 'experience']

            # filter items based on key
            items = []
            for item in json_content['users']:
                filtered_item = {}
                for key in common_keys:
                    filtered_item[key] = json_content[key]
                for key in item_keys:
                    filtered_item[key] = item[key]
                items.append(filtered_item)
            logger.info(f'number of items to be written in ddb: {len(items)}')

            # write items in ddb
            with table.batch_writer() as batch:
                for item in items:
                    batch.put_item(Item=item)
            logger.info(f'wrote {len(items)} items to ddb table')

        return {
            'statusCode': 200,
            'body': 'fetched content from s3 and stored in ddb'
        }
    except Exception as e:
        logger.error(str(e))
        return {
            'statusCode': 500,
            'body': 'something went wrong'
        }
