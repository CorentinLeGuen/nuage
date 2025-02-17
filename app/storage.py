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
        s3_client.put_object(
            Bucket=MINIO_BUCKET,
            Key=file_name,
            Body=file_data.file.read(),
            ContentType=file_data.content_type
        )
        return f"File {file_name} saved on MinIO."
    except NoCredentialsError:
        return "Error: MinIO access refused."
    except Exception as e:
        raise e


def delete_stored_file(file_key):
    try:
        s3_client.delete_object(Bucket=MINIO_BUCKET, Key=file_key)
        return f"File {file_key} deleted."
    except NoCredentialsError:
        return "Error: MinIO access refused."
    except Exception as e:
        raise e


def create_stored_folder(folder_key):
    try:
        s3_client.put_object(Bucket=MINIO_BUCKET, Key=folder_key, Body=b"")
        return f"File {folder_key} deleted."
    except NoCredentialsError:
        return "Error: MinIO access refused."
    except Exception as e:
        raise e


def list_stored_files(user_prefix: str):
    try:
        response = s3_client.list_objects_v2(Bucket=MINIO_BUCKET, Prefix=user_prefix + "/")
        files_by_folder = {}

        if "Contents" in response:
            for obj in response["Contents"]:
                full_path = obj["Key"]
                parts = full_path.split("/")

                folder = parts[1] if len(parts) > 2 else ""
                file_name = parts[-1]
                file_size = obj["Size"]
                file_date = obj["LastModified"].strftime("%Y-%m-%d %H:%M:%S")

                is_folder = file_size == 0 and full_path.endswith("/")

                if folder not in files_by_folder:
                    files_by_folder[folder] = []

                files_by_folder[folder].append(
                    {
                        "file_name": file_name,
                        "size": file_size,
                        "date": file_date,
                        "is_folder": is_folder
                    }
                )

        return files_by_folder
    except Exception as e:
        print(f"MinIO Listing Error: {str(e)}")
        return {}


def download_from_minio(file_key):
    try:
        response = s3_client.get_object(Bucket=MINIO_BUCKET, Key=file_key)
        return response
    except NoCredentialsError:
        return "Error : MinIO access refused."
