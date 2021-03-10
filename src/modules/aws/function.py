import os
import json
import boto3

def invoke(function: str, payload: dict) -> None:
    """Invoke the desired funciton with the given payload

    Args:
        param1 (str) function: The function arn (env variable name)
        param2 (dict) payload: The value that will be sent to the function

    Return:
        Invoke a Lambda function sending the payload to it.
    """    
    lambda_client = boto3.client('lambda')

    lambda_client.invoke(
        FunctionName=os.environ.get(function),
        InvocationType='Event',
        Payload=json.dumps(payload)
    )