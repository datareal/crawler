import io
import re
import lxml
import decimal

from .configurations import CATEGORIES

formated = None

def regex_int(content: str, group: bool = True, index=0, regex_expression=r'\d+'):
    content_sio = io.StringIO(content)
    try:
        parser = lxml.etree.parse(content_sio)

        if content_parsed := parser.xpath('//*/text()'):
            if len(content_parsed) > 1:
                for i in range(len(content_parsed)):
                    if content_integer := re.findall(regex_expression, content_parsed[i]):
                        if group:
                            content_parsed = ''.join(content_integer[j] for j in range(len(content_integer)) if content_integer[i] != '00')

                        else:
                            content_parsed = content_integer[index]
            
                return content_parsed
            
            else:
                if content_integer := re.findall(regex_expression, content_parsed[0]):
                    if group:
                        content_parsed = ''.join(content_integer[j] for j in range(len(content_integer)) if content_integer[0] != '00')

                    else:
                        content_parsed = content_integer[index]
            
                return content_parsed

        else:
            return content

    except Exception:
        if content_parsed := re.findall(regex_expression, content):
            if (content_integer := content_parsed) and (len(content_parsed) > 1):
                if group:
                    content_parsed = ''.join(content_integer[i] for i in range(len(content_integer)) if content_integer[i] != '00')

                else:
                    content_parsed = content_integer[index]

                return content_parsed

            else:
                return content_parsed[0]

        else:
            return content

def cleaner(content: str) -> dict:
    if isinstance(content, decimal.Decimal) or isinstance(content, int):
        content = str(content)

    if isinstance(content, str):
        formated = content.strip()
        formated = formated.replace('\t', '')
        formated = formated.replace('\r', '')
        formated = formated.replace('\n', '')
        formated = formated.replace('<br>', '')

        # The code below is to format Brazil`s numeric model to the Global
        # This code must be deleted when we add global websites
        formated = formated.replace('.', '@')
        formated = formated.replace(',', '!')
        formated = formated.replace('!', '.')
        formated = formated.replace('@', ',')

        return formated.strip()

    return content

def title(content: str) -> str:
    formated = cleaner(content)

    return formated

def price(content: str) -> str:
    formated = cleaner(content)

    if formated := regex_int(formated, regex_expression=r'\d+(?:[\,\.]{0,}\d+)+'):
        formated = formated

    return formated

def rooms(content: str) -> str:
    formated = cleaner(content)

    if formated := regex_int(formated, False):
        formated = formated

    return formated

def suites(content: str) -> str:
    formated = cleaner(content)

    if formated := regex_int(formated, False, 1):
        formated = formated

    return formated

def bathrooms(content: str) -> str:
    formated = cleaner(content)

    if formated := regex_int(formated, False, 1):
        formated = formated

    return formated

def body(content: str) -> str:
    formated = cleaner(content)

    return formated

def category(content: str) -> str:
    formated = cleaner(content.lower())

    for i in range(len(CATEGORIES['Types'])):
        for j in range(len(CATEGORIES[CATEGORIES['Types'][i]])):
            if CATEGORIES[CATEGORIES['Types'][i]][j] in formated:
                formated = CATEGORIES['Types'][i]

    return formated

def features(content: list) -> str:
    formated = list()

    for feature in content:
        if feature.strip():
            formated.append(cleaner(feature))

    return formated

def garages(content: str) -> str:
    formated = cleaner(content)

    if formated_cleansed := re.findall(r'\d+', formated):
        formated_cleansed = ''.join(formated_cleansed[i] for i in range(len(formated_cleansed)))

        try:
            return int(formated_cleansed)

        except Exception:
            pass

    elif not re.findall(r'\d+', formated):
        if 'garage' in formated:
            formated_cleansed = '1'

            try:
                return int(formated_cleansed)

            except Exception:
                pass

    return formated

def total_area(content: str) -> str:
    formated = cleaner(content)

    if formated := regex_int(formated, regex_expression=r'\d+(?:[\d+\,\.]{0,}\d+)+'):
        formated = formated

    return formated

def ground_area(content: str) -> str:
    formated = cleaner(content)

    if formated := regex_int(formated, regex_expression=r'\d+(?:[\d+\,\.]{0,}\d+)+'):
        formated = formated

    return formated

def privative_area(content: str) -> str:
    formated = cleaner(content)

    if formated := regex_int(formated, regex_expression=r'\d+(?:[\d+\,\.]{0,}\d+)+'):
        formated = formated

    return formated

def latitude(content: str) -> str:
    formated = cleaner(content)

    return formated

def longitude(content: str) -> str:
    formated = cleaner(content)

    return formated

def location(content: str) -> str:
    formated = cleaner(content)

    return formated

def address(content: str) -> str:
    formated = cleaner(content)

    return formated

def zipcode(content: str) -> str:
    formated = cleaner(content)

    return formated

def neighbourhood(content: str) -> str:
    formated = cleaner(content)

    return formated

def city(content: str) -> str:
    formated = cleaner(content)

    return formated