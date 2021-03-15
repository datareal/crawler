IGNORE_ITEMS = [
    'item_id',
    'process_id',
    'url',
    's3_uri',
    'domain',
    'date',
    'images',
    'status_code',
    'status'
]

IGNORE_ATTRS = [
    '__class__',
    '__delattr__',
    '__dict__',
    '__dir__',
    '__doc__',
    '__eq__',
    '__format__',
    '__ge__',
    '__getattribute__',
    '__gt__',
    '__hash__',
    '__init__',
    '__init_subclass__',
    '__le__',
    '__lt__',
    '__module__',
    '__ne__',
    '__new__',
    '__reduce__',
    '__reduce_ex__',
    '__repr__',
    '__setattr__',
    '__sizeof__',
    '__str__',
    '__subclasshook__',
    '__weakref__',
    '__slotnames__'
]

CATEGORIES = {
    'Types': ['Apartamentos', 'Casas', 'Comércios', 'Sobrados', 'Galpões', 'Terrenos', 'Salas', 'Lofts'],
    'Apartamentos': ['apartamento', 'apto', 'giardino', 'garden', 'cobertura'],
    'Casas': ['casa', 'residência', 'residencia'],
    'Comércios': ['ponto', 'empreendimento', 'comercial'],
    'Sobrados': ['sobrado', 'geminado'],
    'Galpões': ['galpão', 'galpao'],
    'Terrenos': ['terreno', 'área', 'area', 'rural'],
    'Salas': ['sala'],
    'Lofts': ['loft']
}
