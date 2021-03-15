# item = crawl.get_info(xpaths, content, item)

import parsel

import src.modules.url as URL
import src.modules.models as models

def get_info(xpaths: dict, content: bytes, item: models.Item) -> models.Item:
    parser = parsel.Selector(text=content.decode())

    if 'olx' in item.url:
        return head(xpaths, parser, item)

    else:
        return body(xpaths, parser, item)

def body(xpaths: dict, parser, item: models.Item) -> models.Item:
    item.body: str = parser.xpath(xpaths['parser_body']).extract_first()
    item.title: str = parser.xpath(xpaths['parser_title']).extract_first()
    item.category: str = parser.xpath(xpaths['parser_category']).extract_first()
    item.price: str = parser.xpath(xpaths['parser_price']).extract_first()
    item.rooms: str = parser.xpath(xpaths['parser_rooms']).extract_first()
    item.suites: str = parser.xpath(xpaths['parser_suites']).extract_first()
    item.garages: str = parser.xpath(xpaths['parser_garages']).extract_first()
    item.bathrooms: str = parser.xpath(xpaths['parser_bathrooms']).extract_first()
    item.privative_area: str = parser.xpath(xpaths['parser_privative_area']).extract_first()
    item.total_area: str = parser.xpath(xpaths['parser_total_area']).extract_first()
    item.ground_area: str = parser.xpath(xpaths['parser_ground_area']).extract_first()
    item.address: str = parser.xpath(xpaths['parser_location']).extract_first()
    item.city = parser.xpath(xpaths.get('parser_images_src') or '//parser_city_xyz').extract()
    item.features: str = parser.xpath(xpaths['parser_features']).extract()

    images_src: list = parser.xpath(xpaths['parser_images_src']).extract()
    images_alt: list = parser.xpath(xpaths['parser_images_alt']).extract()
    item.images: list = [
        {
            'src': images_src[i],
            'alt': images_alt[i] or 'Image Alt is empty'
        }
        for i in range(len(images_src))
    ]

    if xpaths.get('options_location_use_geo'):
        item.latitude = parser.xpath(xpaths['parser_location_latitude']).extract_first()
        item.longitude = parser.xpath(xpaths['parser_location_longitude']).extract_first()

    # The following items usually don't have information on the website, so we'll try to fill it to be available on the final Item
    item.city = parser.xpath(xpaths.get('parser_location_city') or '//parser_city_xyz').extract()
    item.zipcode = parser.xpath(xpaths.get('parser_location_zipcode') or '//parser_zipcode_xyz').extract()
    item.neighbourhood = parser.xpath(xpaths.get('parser_location_neighbourhood') or '//parser_neighbourhood_xyz').extract()

    return item