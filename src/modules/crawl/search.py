import parsel

import src.modules.url as URL

def get_items(url: str, xpaths: dict, content: bytes) -> [str, list]:
    parser = parsel.Selector(text=content.decode(xpaths.get('options_encoding') or 'UTF-8'))
    next_page: str = None
    items: [str] = list()

    for item in parser.xpath(xpaths['parser_items']):
        if item := item.xpath(xpaths['parser_items_url']).extract_first():
            if not URL.validator(item):
                item = URL.urljoin(url, item)

            items.append(item)

    next_page = parser.xpath(xpaths['parser_next_page']).extract_first()

    if next_page:
        if not URL.validator(next_page):
            next_page = URL.urljoin(url, next_page)

    return next_page, items