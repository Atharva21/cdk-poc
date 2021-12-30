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
                "siteId": "2040111",
                "origin": "BP",
                "country": "GB",
                "items": [
                    {
                        "barcode": "5012035952808",
                        "linkedItemId": "2039711",
                        "stockOnHand": 10,
                        "availableForSale": True,
                        "lastUpdated": "2020-08-21T14:20:16.000Z",
                        "lastModified": "2020-08-21T14:30:16.000Z",
                        "updateReason": "FullUpdate",
                        "olaCode": "074"
                    },
                    {
                        "barcode": "5012035952809",
                        "linkedItemId": "2039711",
                        "stockOnHand": 10,
                        "availableForSale": True,
                        "lastUpdated": "2020-08-21T14:20:16.000Z",
                        "lastModified": "2020-08-21T14:30:16.000Z",
                        "updateReason": "FullUpdate",
                        "olaCode": "075"
                    },
                    {
                        "barcode": "5012035952811",
                        "linkedItemId": "2039711",
                        "stockOnHand": 10,
                        "availableForSale": True,
                        "lastUpdated": "2020-08-21T14:20:16.000Z",
                        "lastModified": "2020-08-21T14:30:16.000Z",
                        "updateReason": "FullUpdate",
                        "olaCode": "076"
                    }
                ]
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
            self.invoked_function_arn = "arn:aws:lambda:us-east-1:ACCOUNT:function:self.function_name"
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
    # ! 👇 relative import doesnt work?!
    # from ....functions.PublisherFunction import app as publisher
    import src.functions.PublisherFunction.app as publisher
    result = publisher.main(valid_payload, lambda_context)
    assert result == {
        'statusCode': 200,
        'body': 'published message to SQS'
    }
