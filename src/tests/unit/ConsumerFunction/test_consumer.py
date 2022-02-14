import pytest
from moto import mock_s3, mock_dynamodb2
import boto3
from uuid import uuid4
import os
import json


@pytest.fixture(scope="function")
def valid_event():
    yield {
        "Records": [
            {
                "body": json.dumps(
                    {
                        "file_name": "testing.json",
                    }
                ),
            },
        ]
    }


@pytest.fixture(scope="function")
def lambda_context():
    class Lambda_Context:
        def __init__(self):
            self.function_name = "function_name"
            self.function_version = "v$LATEST"
            self.memory_limit_in_mb = 512
            self.invoked_function_arn = (
                "arn:aws:lambda:ap-south-1:ACCOUNT:function:self.function_name"
            )
            self.aws_request_id = str(uuid4())

    yield Lambda_Context()


@pytest.fixture
def mock_aws(valid_payload):
    with mock_s3(), mock_dynamodb2():
        s3boto = boto3.resource("s3", region_name=os.getenv("AWS_REGION"))
        s3boto.create_bucket(
            Bucket=os.getenv("BUCKET_NAME"),
            CreateBucketConfiguration={
                "LocationConstraint": os.getenv("AWS_REGION"),
            },
        )
        s3object = s3boto.Object(os.getenv("BUCKET_NAME"), "testing.json")
        s3object.put(Body=(bytes(valid_payload["body"].encode("UTF-8"))))
        ddb = boto3.resource("dynamodb")
        ddb.create_table(
            TableName=os.getenv("TABLE_NAME"),
            KeySchema=[
                {"AttributeName": "groupId", "KeyType": "HASH"},
                {"AttributeName": "userId", "KeyType": "RANGE"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "groupId", "AttributeType": "S"},
                {"AttributeName": "userId", "AttributeType": "S"},
            ],
        )
        yield


def test_positive_scenario(mock_aws, valid_event, lambda_context):
    from src.functions.ConsumerFunction.app import main as consumer

    result = consumer(valid_event, lambda_context)
    assert result == {
        "statusCode": 200,
        "body": "fetched content from s3 and stored in ddb",
    }
