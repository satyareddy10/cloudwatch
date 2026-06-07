import boto3
import uuid

from django.conf import settings


class S3Service:

    @staticmethod
    def upload_file(file):
        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )

        file_extension = file.name.split('.')[-1]
        file_name = f"products/{uuid.uuid4()}.{file_extension}"

        s3_client.upload_fileobj(
            file,
            settings.AWS_STORAGE_BUCKET_NAME,
            file_name,
            ExtraArgs={
                "ContentType": file.content_type
            }
        )

        return (
            f"https://{settings.AWS_STORAGE_BUCKET_NAME}"
            f".s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/{file_name}"
        )
