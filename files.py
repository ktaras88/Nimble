import boto3
from botocore.exceptions import ClientError
from settings import AWS_SECRET_KEY, AWS_ACCESS_KEY_ID


def s3():
    client = boto3.client(service_name='s3',
                          aws_access_key_id=AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=AWS_SECRET_KEY)
    return client


def upload_file(s3_client, file, bucket, key):
    try:
        s3_client.upload_fileobj(file.file, bucket, key)
    except ClientError as e:
        print(e)
        return False
    return True


def download_file(s3_client, key, bucket):
    try:
        s3_response = s3_client.get_object(Bucket=bucket, Key=key)
        file_content = s3_response["Body"].read()
    except Exception as e:
        print(e)
        return False
    return {'content': file_content, 'media_type': "application/octet-stream"}
