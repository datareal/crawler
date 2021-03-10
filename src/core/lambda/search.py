import json

import src.modules.url as URL
import src.modules.crawl as crawl
import src.modules.header as Header
import src.modules.request as request
import src.modules.exceptions as exceptions

xpaths = {
    "domain": "anageimoveis.com.br",
    "id": "288864e4-553a-4094-99a4-3b3934ea219f",
    "parser_arguments_render": "false",
    "parser_arguments_wait": "true",
    "parser_arguments_wait_time": "30.0",
    "parser_items": "//*[@id='block-result-search']/section/div[@class='cards-list']//article[contains(@class,'bloco')]",
    "parser_items_url": ".//span[contains(@class,'img')]/a[contains(@class,'lk-img')]/@href",
    "parser_next_page": "//*[@id=\"block-result-search\"]/section//span/a[text()='Próxima página']/@href",
    "parser_url_string": "page="
}

def handler(event: dict, context) -> dict:
    url: str = event.get('url')

    if not url:
        raise exceptions.NoURLProvided("You must provide an URL to lambda:search")
    
    if not URL.validator(url):
        raise exceptions.NoValidURL("You must provide a valide URL to lambda:search")

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