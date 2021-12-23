from ....functions.PublisherFunction import app as publisher


def test_sample():
    result = publisher.main()
    assert result == {
        'statusCode': 200,
        'body': 'published message to SQS'
    }
