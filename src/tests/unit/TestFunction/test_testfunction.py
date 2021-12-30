import boto3
from moto import mock_s3


@mock_s3
def test_main():
    _s3 = boto3.resource('s3')
    _s3.create_bucket(Bucket='testing', CreateBucketConfiguration={
        'LocationConstraint': 'ap-south-1',
    })
    from src.functions.TestFunction.app import main
    result = main(None, None)
    assert result == 1
