import copy
import uuid
import json

import src.modules.aws as aws
import src.modules.url as URL
import src.modules.crawl as crawl
import src.modules.models as models
import src.modules.header as Header
import src.modules.request as request
import src.modules.storage as storage
import src.modules.database as database
import src.modules.sanitizer as sanitizer
import src.modules.exceptions as exceptions

def handler(event: dict, content) -> dict:
    item = models.Item()
    item.date = item.date
    item.item_id: str = event.get('id') or str(uuid.uuid4())
    item.process_id: str = event.get('process') or str(uuid.uuid4()) # Receiving `process` attribute from event request is only valid when reprocessing

    bucket: str = 'datareal-crawler-bodies'
    path: str = None
    filename: str = None

    content: bytes

    if not event.get('url'):
        raise exceptions.NoURLProvided("You must provide an URL to lambda:item")

    if not URL.validator(event.get('url')):
        raise exceptions.NoValidURL("You must provide a valide URL to lambda:item")

    item.url: str = event.get('url')
    item.domain: str = URL.extract_domain(item.url)
    item.s3_uri = event.get('s3_uri')

    action: str = event.get('action') or 'ADD'
    item.status = action

    xpaths = database.query('ITEM_CONFIG_TABLE', {
        'index': 'domain-index',
        'key': 'domain',
        'value': item.domain
    })

    if action == 'ADD' or action == 'UPDATE':
        header = Header.Header()
        response = request.Request(
            item.url,
            header=header.headers,
            render=xpaths.get('options_use_render') or False,
            method='GET',
            encoding='UTF-8'
        ).fetch()

        content = response.content
        item.status_code = response.status_code

    elif action == 'REPROCESS':
        bucket, *object_key = storage.split_s3_uri(item.s3_uri)

        content = storage.download(
            bucket,
            object_key[0],
            object_key[1]
        )

        item.status_code = event.get('status_code')

    else:
        raise Exception(f"Unknow action: {action}.\nKnown actions: [ADD, UPDATE, REPROCESS]")

    if content == bytes(0x0001):
        raise Exception('Not found anything on S3.')

    elif not content:
        raise exceptions.EmptyBody('The body content is empty. Ignoring crawl since it has already been crawled today.')

    if item.status_code == 200:
        item = crawl.get_info(xpaths, content, item)
        item = sanitizer.clean(item)

    else:
        item.status = 'OFFLINE'

    # This will just save the HTML content on S3 if it's not reprocessing
    if not action == 'REPROCESS':
        if not filename:
            object_path = storage.filename_from_url(item.url)
            path = object_path['folder']
            filename = object_path['file']

        item.s3_uri = f"s3://{bucket}/{path}/{filename}"
        storage.save(content, bucket, path, filename)

    print('Item content', vars(item))

    # This will create a DeepCopy of the item object in another address in the memory without referencing to the original item
    unique_item = models.convert_to_database_dict(copy.deepcopy(item))
    rawdata_item = models.convert_to_database_dict(item)

    del unique_item['process']
    del unique_item['date']

    if action == 'UPDATE':
        database.put('RAWDATA_TABLE', rawdata_item)
        database.update('UNIQUE_RAWDATA_TABLE', unique_item, {
            'Key': {
                'id': unique_item['id'],
                'url': unique_item['url']
            }
        })

    elif action == 'REPROCESS':
        database.update('RAWDATA_TABLE', rawdata_item, {
            'Key': {
                'id': rawdata_item['id'],
                'process': rawdata_item['process']
            }
        })
        database.update('UNIQUE_RAWDATA_TABLE', unique_item, {
            'Key': {
                'id': unique_item['id'],
                'url': unique_item['url']
            }
        })

    elif action == 'ADD':
        database.put('RAWDATA_TABLE', rawdata_item)
        database.put('UNIQUE_RAWDATA_TABLE', unique_item)

    return {
        "status_code": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "ID": item.item_id,
            "ProcessID": item.process_id,
            "Action": action
        })
    }