import json
import boto3
from botocore.exceptions import ClientError

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
table_name = 'FileProcessingStatus'  # Replace with your table name
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    both_loaded = False  # Initialize the variable
    account_loaded = False
    transaction_loaded = False

    try:
        # Check if both account and transaction files have been loaded
        account_response = table.get_item(
            Key={
                'fileType': 'account',
                'statusType': 'loaded'
            }
        )
        
        transaction_response = table.get_item(
            Key={
                'fileType': 'transaction',
                'statusType': 'loaded'
            }
        )

        # Determine if both tables are loaded
        account_loaded = 'Item' in account_response and account_response['Item'].get('loaded', False)
        transaction_loaded = 'Item' in transaction_response and transaction_response['Item'].get('loaded', False)

        both_loaded = account_loaded and transaction_loaded

        return {
            'bothLoaded': both_loaded,
            'accountLoaded': account_loaded,
            'transactionLoaded': transaction_loaded
        }

    except ClientError as e:
        print(f"Error checking tables loaded: {e.response['Error']['Message']}")
        return {
            'bothLoaded': both_loaded,
            'accountLoaded': account_loaded,
            'transactionLoaded': transaction_loaded
        }
