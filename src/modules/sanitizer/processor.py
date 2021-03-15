import importlib
from .configurations import IGNORE_ATTRS
from .configurations import IGNORE_ITEMS

def clean(item: object) -> object:
    for attribute in dir(item):
        if not attribute in IGNORE_ATTRS and not attribute in IGNORE_ITEMS:
            attribute_value = getattr(item, attribute, 'Attribute not found.')  
            function = getattr(importlib.import_module('src.modules.sanitizer.cleaner'), attribute)

            try:
                if attribute_value:
                    setattr(item, attribute, function(attribute_value))

            except TypeError:
                print(f"Error when sanitizing attribute {attribute}{type(attribute_value)} with <{attribute_value}> as its value")

    return item