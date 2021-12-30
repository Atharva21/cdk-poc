import boto3
import json

_s3 = boto3.resource('s3')


def main(event, context):
    s3object = _s3.Object('testing', 'filename')
    s3object.put(
        Body=(bytes(json.dumps('yo').encode('UTF-8')))
    )
    return 1
