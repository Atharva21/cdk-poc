import boto3
import pytest
from moto import mock_s3


@pytest.fixture
def mock_aws():
    print('mock start')
    with mock_s3():
        foo = 'bar'
        yield foo
    print('mock end')


# @mock_s3
def test_main(mock_aws):
    print(mock_aws)
    _s3 = boto3.resource('s3')
    _s3.create_bucket(Bucket='testing', CreateBucketConfiguration={
        'LocationConstraint': 'ap-south-1',
    })
    from src.functions.TestFunction.app import main
    result = main(None, None)
    assert result == 1
    print('test one end')


def test_other(mock_aws):
    assert 1 == 1
    print('test two end')
