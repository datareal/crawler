import os
import boto3

def put(table: str, item: dict) -> None:
    dynamodb_client = boto3.resource('dynamodb')
    dynamodb_table = dynamodb_client.Table(os.environ.get(table))

    dynamodb_table.put_item(
        Item=item
    )

def update(table: str, item: dict, key: dict) -> dict:
    """Update a item on DynamoDB table

    Args:
        param1 (str) table: The target table to update the item
        param2 (dict) item: The new item - Reference: src.modules.models.Item
        param3 (dict) key: The item key
            Should look like this:
            - {
                'Key': {
                    'hash_key': 'hash_value',
                    'sort_key': 'sort_value'
                }
            }
    """

    dynamodb_client = boto3.resource('dynamodb')
    dynamodb_table = dynamodb_client.Table(os.environ.get(table))

    args = {
        **key,
        'UpdateExpression': 'SET #tit=:tit, #cat=:cat, #bod=:bod, #roo=:roo, #sui=:sui, #gar=:gar, #bat=:bat, #pri=:pri, #fea=:fea, #cit=:cit, #add=:add, #nei=:nei, #zip=:zip, #lat=:lat, #lon=:lon, #tot=:tot, #gro=:gro, #prv=:prv, #ima=:ima, #sta=:sta',
        'ExpressionAttributeValues': {
            ':tit': item['title'],
            ':cat': item['category'],
            ':bod': item['body'],
            ':roo': item['rooms'],
            ':sui': item['suites'],
            ':gar': item['garages'],
            ':bat': item['bathrooms'],
            ':pri': item['price'],
            ':fea': item['features'],
            ':cit': item['city'],
            ':add': item['address'],
            ':nei': item['neighbourhood'],
            ':zip': item['zipcode'],
            ':lat': item['latitude'],
            ':lon': item['longitude'],
            ':tot': item['total_area'],
            ':gro': item['ground_area'],
            ':prv': item['privative_area'],
            ':ima': item['images'],
            ':sta': item['status']
        },
        'ExpressionAttributeNames': {
            '#tit': 'title',
            '#cat': 'category',
            '#bod': 'body',
            '#roo': 'rooms',
            '#sui': 'suites',
            '#gar': 'garages',
            '#bat': 'bathrooms',
            '#pri': 'price',
            '#fea': 'features',
            '#cit': 'city',
            '#add': 'address',
            '#nei': 'neighbourhood',
            '#zip': 'zipcode',
            '#lat': 'latitude',
            '#lon': 'longitude',
            '#tot': 'total_area',
            '#gro': 'ground_area',
            '#prv': 'privative_area',
            '#ima': 'images',
            '#sta': 'status'
        },
        'ReturnValues': 'UPDATED_NEW'
    }

    try:
        # The update_item function will receive a dictionary that will be passed as kwargs
        response = dynamodb_table.update_item(**args)
    
    except Exception as error:
        raise Exception(f'Error when updating item {error}. UpdateItem args: {args}.')
    
    else:
        return response