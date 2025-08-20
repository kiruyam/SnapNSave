import json
import boto3
import os
from botocore.exceptions import ClientError

s3_client = boto3.client("s3")
BUCKET_NAME = os.environ.get("UPLOAD_BUCKET", "your-s3-bucket-name")

def lambda_handler(event, context):
    try:
        # Extract user identity from Cognito (if using Authorizer)
        user_id = event["requestContext"]["authorizer"]["claims"]["sub"]

        # Get file name from query/body
        body = json.loads(event["body"])
        file_name = body.get("file_name")
        if not file_name:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "file_name is required"})
            }

        # Generate a pre-signed URL for PUT operation
        presigned_url = s3_client.generate_presigned_url(
            "put_object",
            Params={
                "Bucket": BUCKET_NAME,
                "Key": f"{user_id}/{file_name}"
            },
            ExpiresIn=3600
        )

        return {
            "statusCode": 200,
            "body": json.dumps({
                "upload_url": presigned_url,
                "file_key": f"{user_id}/{file_name}"
            })
        }

    except ClientError as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
