import json
from typing import Any, Dict
import boto3
import uuid
import os
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools import Logger, Metrics, Tracer
from .foo import yolo

_queue_name = os.getenv("QUEUE_NAME")
_bucket_name = os.getenv("BUCKET_NAME")

_s3 = boto3.resource("s3")
_sqs = boto3.resource("sqs")
_queue = _sqs.get_queue_by_name(QueueName=_queue_name)

logger = Logger()
tracer = Tracer()
metrics = Metrics()


@metrics.log_metrics(capture_cold_start_metric=True)
@logger.inject_lambda_context
@tracer.capture_lambda_handler
def main(event: Dict[str, Any], context: LambdaContext):
    request_id = context.aws_request_id or uuid.uuid4()
    logger.structure_logs(append=True, requestId=request_id)
    try:
        # write body to s3 bucket
        logger.info(yolo)
        body = json.loads(event["body"])
        logger.info(f"producer lambda called with requestId {request_id}")
        filename = f"{uuid.uuid4()}.json"
        s3object = _s3.Object(_bucket_name, filename)
        s3object.put(Body=(bytes(json.dumps(body).encode("UTF-8"))))
        logger.info(f"put {filename} into s3 bucket.")

        # send filename to sqs.
        _queue.send_message(MessageBody=json.dumps({"file_name": filename}))
        logger.info(f"sent {filename} to sqs")

        return {"statusCode": 200, "body": "published message to SQS"}
    except Exception as e:
        logger.error(str(e))
        return {"statusCode": 500, "body": "something went wrong"}
