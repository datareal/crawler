import json
import datetime

import src.modules.aws as aws
import src.modules.url as URL
import src.modules.storage as storage
import src.modules.database as database

def handler(event: dict, content) -> dict:
    items = list()
    item_payload = dict()
    urls: list = event.get('urls')

    for url in urls:
        item_payload['url'] = url
        item_payload['action'] = 'ADD'

        # Verify on Unique Rawdata
        unique_rawdata_query = {
            'table': 'UNIQUE_RAWDATA_TABLE',
            'query': {
                'index': 'url-index',
                'key': 'url',
                'value': URL.extract_domain(url)
            }
        }
        if unique_rawdata_item := database.query(**unique_rawdata_query):
            item_payload['id'] = unique_rawdata_item['id']
            item_payload['action'] = 'UPDATE'

            # Verify on Rawdata Table
            rawdata_query = {
                'table': 'RAWDATA_TABLE',
                'query': {
                    'index': 'url-date-index',
                    'hash_key': 'url',
                    'hash_value': URL.extract_domain(url),
                    'sort_key': 'date',
                    'sort_value': datetime.datetime.today().strftime("%Y-%m-%d")
                }
            }
            if rawdata_item := database.query(**rawdata_query):
                object_path = storage.filename_from_url(url)
                item_payload['s3_uri'] = f"s3://datareal-crawler-bodies/{object_path['path']/{object_path['filename']}}"
                item_payload['action'] = 'REPROCESS'

        aws.invoke('ITEM_FUNCTION', item_payload)
        items.append(item_payload)

    return {
        "status_code": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "Items": items
        })
    }