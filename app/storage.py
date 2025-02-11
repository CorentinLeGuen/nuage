import boto3
from botocore.exceptions import NoCredentialsError
from app.config import MINIO_ENDPOINT, MINIO_ROOT_USER, MINIO_ROOT_PASSWORD, MINIO_BUCKET

s3_client = boto3.client(
    "s3",
    endpoint_url=MINIO_ENDPOINT,
    aws_access_key_id=MINIO_ROOT_USER,
    aws_secret_access_key=MINIO_ROOT_PASSWORD,
)

def create_bucket():
    try:
        s3_client.head_bucket(Bucket=MINIO_BUCKET)
    except Exception:
        s3_client.create_bucket(Bucket=MINIO_BUCKET)

create_bucket()

def upload_to_minio(file_name, file_data):
    try:
        s3_client.put_object(Bucket=MINIO_BUCKET, Key=file_name, Body=file_data)
        return f"File {file_name} saved on MinIO."
    except NoCredentialsError:
        return "Error : MinIO access refused."

def download_from_minio(file_name):
    try:
        response = s3_client.get_object(Bucket=MINIO_BUCKET, Key=file_name)
        return response["Body"].read()
    except NoCredentialsError:
        return "Error : MinIO access refused."
