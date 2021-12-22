import json, boto3, uuid, os

_queue_name = os.getenv('QUEUE_NAME')
_bucket_name = os.getenv('BUCKET_NAME')

s3 = boto3.resource('s3')
sqs = boto3.resource('sqs')
queue = sqs.get_queue_by_name(QueueName=_queue_name)

def main(event, _):
	body = json.loads(event['body'])
	uid = uuid.uuid4()
	s3object = s3.Object(_bucket_name, f'{uid}.json')
	s3object.put(
		Body=(bytes(json.dumps(body).encode('UTF-8')))
	)
	queue.send_message(MessageBody=json.dumps({
		'file_name': f'{uid}.json'
	}))
	return {
		'statusCode': 200,
		'body': 'published message to SQS'
	}