import pytest
import os


@pytest.fixture(scope="package", autouse=True)
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_REGION"] = "ap-south-1"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["POWERTOOLS_METRICS_NAMESPACE"] = "testing"
    os.environ["POWERTOOLS_TRACE_DISABLED"] = '1'


@pytest.fixture(scope="package", autouse=True)
def mock_envs():
    "resource variables"
    os.environ['BUCKET_NAME'] = 'test-bucket'
    os.environ['TABLE_NAME'] = 'test-table'
    os.environ['QUEUE_NAME'] = 'test-queue'
