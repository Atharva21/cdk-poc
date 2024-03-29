import json
from typing import Dict
from uuid import uuid4
import pytest
import os
import warnings


@pytest.fixture(scope="package", autouse=True)
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_REGION"] = "ap-south-1"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "ap-south-1"
    os.environ["POWERTOOLS_SERVICE_NAME"] = "cdk-poc"
    os.environ["POWERTOOLS_METRICS_NAMESPACE"] = "cdk-poc"
    os.environ["POWERTOOLS_METRICS_NAMESPACE"] = "cdk-poc"
    os.environ["POWERTOOLS_TRACE_DISABLED"] = "1"


@pytest.fixture(scope="function")
def valid_payload() -> Dict:
    yield {
        "body": json.dumps(
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


@pytest.fixture(scope="package", autouse=True)
def mock_envs():
    "resource variables"
    os.environ["BUCKET_NAME"] = "test-bucket"
    os.environ["TABLE_NAME"] = "test-table"
    os.environ["QUEUE_NAME"] = "test-queue"


@pytest.fixture(scope="function", autouse=True)
def disable_metric_warning():
    warnings.filterwarnings("ignore", "No metrics to publish*")
