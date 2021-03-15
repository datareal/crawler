from .item import Item

def convert_to_database_dict(item: Item) -> dict:
    item = item.__dict__

    item['id'] = item.pop('item_id')
    item['process'] = item.pop('process_id')

    return item