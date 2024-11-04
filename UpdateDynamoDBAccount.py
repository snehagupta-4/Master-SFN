import json
import boto3
from botocore.exceptions import ClientError

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
table_name = 'FileProcessingStatus'  # Replace with your table name
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    try:
        # Update the loading status for the account file
        response = table.update_item(
            Key={
                'fileType': 'account',        # Fixed key for account file type
                'statusType': 'loaded'         # Fixed sort key for loaded status
            },
            UpdateExpression="SET loaded = :val, lastUpdated = :time",
            ExpressionAttributeValues={
                ':val': True,                # Set loaded to True
                ':time': context.aws_request_id  # Use request ID as a timestamp for simplicity
            },
            ReturnValues="UPDATED_NEW"      # Return the updated attributes
        )

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Account loading status updated successfully',
                'updatedAttributes': response['Attributes']
            })
        }

    except ClientError as e:
        print(f"Error updating account loading status: {e.response['Error']['Message']}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Could not update account loading status'})
        }
