import os
import boto3
from botocore import exceptions
from boto3.dynamodb import conditions

from src.modules.exceptions import DynamoDB

def scan(table: str, query: dict = dict()) -> list:
    """Scan the desired table using kwargs
    
    Args:
        param1 (str) table: The DynamoDB Table name
        param2 (dict) query: The target query options

    Return:
        The response Items from DynamoDb which matches the query
        and the LastEvaluatedKey if exists
    """
    result = list()
    start_key = None
    done = False

    dynamodb_client = boto3.resource('dynamodb')
    dynamodb_table = dynamodb_client.Table(os.environ.get(table))

    try:
        while not done:
            if start_key:
                query['ExclusiveStartKey'] = start_key
            response = dynamodb_table.scan(**query)
            result.extend(response.get('Items', []))
            start_key = response.get('LastEvaluatedKey', None)
            done = start_key is None

    except exceptions.ClientError as error:
        raise DynamoDB.ClientError(f'Error when scanning Dynamo {table} with query {query}\n\n{error}')

    else:
        if result: 
            return result[0]
        else: 
            return dict()

def query(table: str, query: dict) -> dict:
    """Query the desired table using kwargs
    
    Args:
        param1 (str) table: The DynamoDB Table name
        param2 (dict) query: The target query options
            {
                index: The Table GSI,
                key: The primary key of the index,
                value: The value of the key to query on the Table
            }

            or 

            {
                index: The Table GSI,
                hash_key: The primary key of the index,
                hash_value: The value of the primary key to query on the Table
                sort_key: The sort key of the index,
                sort_value: The value of the sort key to query on the Table
            }

    Return:
        The response Items from DynamoDb which matches the query
        and the LastEvaluatedKey if exists
    """
    result = list()
    start_key = None
    done = False

    dynamodb_client = boto3.resource('dynamodb')
    dynamodb_table = dynamodb_client.Table(os.environ.get(table))

    query_kwargs = {
        'IndexName': query.get('index')
    }

    if query.get('sort_key'):
        query_kwargs['KeyConditionExpression'] = conditions.Key(query.get('hash_key')).eq(query.get('hash_value')) & conditions.Key(query.get('range_key')).eq(query.get('range_value'))

    else:
        query_kwargs['KeyConditionExpression'] = conditions.Key(query.get('key')).eq(query.get('value'))

    try:
        while not done:
            if start_key:
                query_kwargs['ExclusiveStartKey'] = start_key
            response = dynamodb_table.query(**query_kwargs)
            result.extend(response.get('Items', []))
            start_key = response.get('LastEvaluatedKey', None)
            done = start_key is None

    except exceptions.ClientError as error:
        raise DynamoDB.ClientError(f'Error when quering Dynamo {table} with query {query}\n\n{error}')

    else:
        if result:
            return result[0]
        else:
            return dict()