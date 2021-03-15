import json
import datetime

import os

import src.modules.aws as aws
import src.modules.url as URL
import src.modules.storage as storage
import src.modules.database as database

def handler(event: dict, content) -> dict:
    items = list()
    urls: list = event.get('urls')

    for url in urls:
        item_payload = dict()
        item_payload['url'] = url
        item_payload['action'] = 'ADD'

        # Verify on Unique Rawdata
        if unique_rawdata_item := database.query('UNIQUE_RAWDATA_TABLE', {
            'index': 'url-index',
            'key': 'url',
            'value': url
        }):
            item_payload['id'] = unique_rawdata_item['id']
            item_payload['action'] = 'UPDATE'

            # Verify on Rawdata Table
            if rawdata_item := database.query('RAWDATA_TABLE', {
                'index': 'url-date-index',
                'hash_key': 'url',
                'hash_value': url,
                'sort_key': 'date',
                'sort_value': datetime.datetime.today().strftime("%Y-%m-%d")
            }):
                item_payload['process'] = rawdata_item['process']
                item_payload['s3_uri'] = rawdata_item['s3_uri']
                item_payload['status_code'] = int(rawdata_item['status_code'])
                item_payload['action'] = 'REPROCESS'

        aws.invoke('ITEM_FUNCTION', item_payload)
        items.append(item_payload)

    print({
        "status_code": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": {
            "items": items
        }
    })

    return {
        "status_code": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "Items": items
        })
    }