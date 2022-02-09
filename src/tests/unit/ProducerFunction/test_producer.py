from typing import Dict, NamedTuple
import pytest
import os
import json
from moto import mock_s3, mock_sqs
from uuid import uuid4
import boto3


@pytest.fixture(scope="function")
def valid_payload() -> Dict:
    yield {
        'body': json.dumps(
            {
                "groupId": str(uuid4()),
                "groupName": str(uuid4()),
                "region": "india",
                "users": [
                    {
                        "userId": str(uuid4()),
                        "hobby": "chess",
                        "experience": 2,
                    },
                    {
                        "userId": str(uuid4()),
                        "hobby": "basketball",
                        "experience": 1,
                    },
                ],
            }
        )
    }


@pytest.fixture(scope='function')
def lambda_context():
    class Lambda_Context:
        def __init__(self):
            self.function_name = 'function_name'
            self.function_version = "v$LATEST"
            self.memory_limit_in_mb = 512
            self.invoked_function_arn = "arn:aws:lambda:ap-south-1:ACCOUNT:function:self.function_name"
            self.aws_request_id = str(uuid4())
    yield Lambda_Context()


@pytest.fixture
def mock_aws():
    with mock_s3(), mock_sqs():
        s3boto = boto3.resource('s3', region_name='ap-south-1')
        sqs_boto = boto3.resource('sqs')
        sqs_boto.create_queue(QueueName=os.getenv('QUEUE_NAME'))
        s3boto.create_bucket(Bucket=os.getenv('BUCKET_NAME'), CreateBucketConfiguration={
            'LocationConstraint': os.getenv('AWS_REGION'),
        })
        yield


def test_positive_scenario(mock_aws, valid_payload, lambda_context):
    # ! 👇 relative import doesn't work?!
    # from ....functions.Producer import app as producer
    from src.functions.ProducerFunction.app import main as producer
    result = producer(valid_payload, lambda_context)
    assert result == {
        'statusCode': 200,
        'body': 'published message to SQS'
    }
