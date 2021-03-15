import io
import boto3

def save(content: bytes, bucket: str, path: str, filename: str) -> str:
    client = boto3.client('s3')
    object_path = f"{path}/{filename}"

    client.upload_fileobj(io.BytesIO(content), bucket, object_path)