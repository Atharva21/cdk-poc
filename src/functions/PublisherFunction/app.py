import json
import boto3
import uuid
import os
from aws_lambda_powertools import Logger, Metrics, Tracer

_queue_name = os.getenv('QUEUE_NAME')
_bucket_name = os.getenv('BUCKET_NAME')

s3 = boto3.resource('s3')
sqs = boto3.resource('sqs')
queue = sqs.get_queue_by_name(QueueName=_queue_name)

logger = Logger()
tracer = Tracer()
metrics = Metrics()


@metrics.log_metrics(capture_cold_start_metric=True)
@logger.inject_lambda_context
@tracer.capture_lambda_handler
def main(event, _):
    logger.info('hello from logger')
    body = json.loads(event['body'])
    filename = f'{uuid.uuid4()}.json'
    s3object = s3.Object(_bucket_name, filename)
    s3object.put(
        Body=(bytes(json.dumps(body).encode('UTF-8')))
    )
    queue.send_message(MessageBody=json.dumps({
        'file_name': filename
    }))
    return {
        'statusCode': 200,
        'body': 'published message to SQS'
    }
