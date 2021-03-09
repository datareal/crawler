import json

import src.modules.aws as aws
import src.modules.url as URL
import src.modules.database as database
import src.modules.exceptions as exceptions

def handler(event: dict, context) -> dict:
    url: str = event.get('url')

    if not url:
        items = database.scan('REAL_ESTATE_TABLE')

    else:
        items = database.query('REAL_ESTATE_TABLE', {
            'index': 'domain-index',
            'key': 'domain',
            'value': URL.extract_domain(url)
        })

    for item in items:
        for url in item.get('urls'):
            print(url)

    return {
        "status_code": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "Items": items
        })
    }