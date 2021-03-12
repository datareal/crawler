import json

import src.modules.aws as aws
import src.modules.url as URL
import src.modules.crawl as crawl
import src.modules.header as Header
import src.modules.request as request
import src.modules.database as database
import src.modules.exceptions as exceptions

def handler(event: dict, context) -> dict:
    url: str = event.get('url')

    if not url:
        raise exceptions.NoURLProvided("You must provide an URL to lambda:search")
    
    if not URL.validator(url):
        raise exceptions.NoValidURL("You must provide a valide URL to lambda:search")

    xpaths = database.query('SEARCH_CONFIG_TABLE', {
        'index': 'domain-index',
        'key': 'domain',
        'value': URL.extract_domain(url)
    })

    header = Header.Header()
    response = request.Request(
        url,
        header=header.headers,
        render=xpaths.get('options_use_render') or False,
        method='GET',
        encoding='UTF-8'
    ).fetch()

    next_page, items = crawl.get_items(url, xpaths, response.content)

    print({
        "body": {
            "Items": items,
            "NextPage": next_page
        }
    })

    aws.invoke('VERIFIER_FUNCTION', {'urls': items})
    aws.invoke('DAEMON', {'target': 'SEARCH_FUNCTION', 'payload': {'url': next_page}})

    return {
        "status_code": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "Items": items,
            "NextPage": next_page
        })
    }