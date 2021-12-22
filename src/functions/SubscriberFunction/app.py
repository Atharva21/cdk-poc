import json, boto3, os

_table_name = os.getenv('TABLE_NAME')
_bucket_name = os.getenv('BUCKET_NAME')

s3 = boto3.resource('s3')
ddb = boto3.resource('dynamodb')
table = ddb.Table(_table_name)

def main(event, _):
	message_body = json.loads(event['Records'][0]['body'])
	s3object = s3.Object(_bucket_name, message_body['file_name'])
	file_content = s3object.get()['Body'].read().decode('utf-8')
	json_content = json.loads(file_content)

	common_keys = ['siteId', 'origin', 'country']
	item_keys = ['barcode', 'linkedItemId', 'stockOnHand', 'availableForSale', 'lastUpdated', 'lastModified', 'updateReason', 'olaCode']
	items = []
	for item in json_content['items']:
		filtered_item = {}
		for key in common_keys:
			filtered_item[key] = json_content[key]
		for key in item_keys:
			filtered_item[key] = item[key]
		items.append(filtered_item)

	with table.batch_writer() as batch:
		for item in items:
			batch.put_item(Item=item)

	return {
		'statusCode': 200,
		'body': 'fetched content from s3 and stored in ddb'
	}