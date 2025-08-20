import json
import boto3
import os
from botocore.exceptions import ClientError
from decimal import Decimal

# Initialize AWS clients
textract_client = boto3.client("textract")
dynamodb = boto3.resource("dynamodb")
ses_client = boto3.client("ses")

# Environment variables
TABLE_NAME = os.environ.get("BILLS_TABLE", "BillsTable")
EMAIL_SENDER = os.environ.get("EMAIL_SENDER", "your-email@example.com")

table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    try:
        # Loop over each S3 event record
        for record in event["Records"]:
            bucket_name = record["s3"]["bucket"]["name"]
            file_key = record["s3"]["object"]["key"]

            # Extract user_id from file path (format: user_id/filename.jpg)
            user_id = file_key.split("/")[0]

            print(f"Processing file: {file_key} from bucket: {bucket_name}")

            # Call Textract to extract text
            response = textract_client.detect_document_text(
                Document={"S3Object": {"Bucket": bucket_name, "Name": file_key}}
            )

            # Extract text lines
            extracted_text = []
            for block in response["Blocks"]:
                if block["BlockType"] == "LINE":
                    extracted_text.append(block["Text"])

            extracted_text_str = "\n".join(extracted_text)

            # Store in DynamoDB
            item = {
                "user_id": user_id,
                "file_key": file_key,
                "extracted_text": extracted_text_str,
            }

            table.put_item(Item=json.loads(json.dumps(item), parse_float=Decimal))

            # Send confirmation email (optional)
            try:
                ses_client.send_email(
                    Source=EMAIL_SENDER,
                    Destination={"ToAddresses": [EMAIL_SENDER]},  # You can replace with user email if mapped
                    Message={
                        "Subject": {"Data": f"Receipt Processed for {user_id}"},
                        "Body": {
                            "Text": {"Data": f"File {file_key} processed.\nExtracted text:\n{extracted_text_str}"}
                        },
                    },
                )
            except ClientError as e:
                print(f"SES Error: {str(e)}")

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Receipts processed successfully"})
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
