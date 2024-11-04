import json
import boto3
from botocore.exceptions import ClientError

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
table_name = 'FileProcessingStatus'
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    try:
        # Scan the table to get all items
        response = table.scan()
        items = response.get('Items', [])

        if not items:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'No items found in the table'})
            }

        # Sort items by lastUpdated timestamp
        items.sort(key=lambda x: x.get('lastUpdated', ''))
        locked_files = ""
        # Lock all items except the one with the earliest lastUpdated timestamp
        for item in items[1:]:
            file_type = item['fileType']
            status_type = item['statusType']

            # Check if the item is already locked
            if item.get('locked', False):
                continue

            # Update the item to set locked to true
            table.update_item(
                Key={
                    'fileType': file_type,
                    'statusType': status_type
                },
                UpdateExpression="SET locked = :val",
                ExpressionAttributeValues={
                    ':val': True
                },
                ReturnValues="UPDATED_NEW"
            )
            if locked_files:
                locked_files += ","  # Add a comma for subsequent entries
            locked_files += file_type

        return {
            'statusCode': 200,
            'lockedFiles': locked_files
        }

    except ClientError as e:
        print(f"Error locking files: {e.response['Error']['Message']}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Could not lock files'})
        }
