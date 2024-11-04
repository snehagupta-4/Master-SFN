import json
import boto3
from botocore.exceptions import ClientError

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
table_name = 'FileProcessingStatus'  # Replace with your table name
#table_name = 'DDSL_Dynamodb'  # Replace with your table name
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
   # primary_key_value = event['transaction', 'loaded']  # Get the primary key from the event
   # new_data = event['transaction', 'locked']  # The data you want to update
    
   # current_timestamp = int(time.time() * 1000)  # Current time in milliseconds
    try:
        # Update the loading status for the transaction file
        response = table.update_item(
            Key={
                'fileType': 'transaction',    # Fixed key for transaction file type
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
                'message': 'Transaction loading status updated successfully',
                'updatedAttributes': response['Attributes']
            })
        }

    except ClientError as e:
        print(f"Error updating transaction loading status: {e.response['Error']['Message']}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Could not update transaction loading status'})
        }
