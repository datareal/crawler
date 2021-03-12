import boto3
import hashlib
import datetime
from botocore import exceptions

import src.modules.url as URL

def download(bucket: str, path: str, filename: str) -> bytes:
    """Verify if the given S3 object exists in the bucket

    Args:
        param1 (str) bucket: The bucket name to verify for
        param2 (str) path: The path for the object
        param3 (str) filename: The name of the object

    Return:
        If the object exist it return True, and if not it return False
    """
    client = boto3.resource('s3')
    response: bytes

    try:
        obj = client.Object(bucket_name=bucket, key=f'{path}/{filename}').get()

    except exceptions.ClientError as error:
        if error.response['Error']['Code'] == 'NoSuchKey':
            response = bytes(0)

        else:
            print(error)
            raise Exception('Something went wrong searching for file in S3 Bucket.')
    else:
        response = obj['body'].read()
    
    return response


def filename_from_url(url: str) -> dict:
        """Create the S3 object filename from the given URL

        Args:
            param1 (str) url: The url to get the path and filename

        Return:
            A dict with path and filename that is referent to the S3 object
        """
        domain = URL.extract_domain(url=url)
        path = URL.extract_path(url=url)

        folder = hashlib.md5(domain.encode()).hexdigest()
        file = hashlib.md5(path.encode()).hexdigest()

        return {
            'folder': f'{folder}/{file}',
            'file': datetime.datetime.today().strftime("%Y-%m-%d") + '.body'
        }
