import re
import w3lib.url
import urllib.parse

def escape_ajax(url: str) -> str:
    """Docstring for the escape_ajax function.
    
    Escape special characters to make AJAX requests.

    Args:
        param1 (str) url:
            The url to escape the AJAX

    Returns:
        Escaped url (str).
    """
    defrag, frag = urllib.parse.urldefrag(url)
    if not frag.startswith('!'):
        return url

    return w3lib.url.add_or_replace_parameter(defrag, '_escaped_fragment_', frag[1:])

def validator(url: str) -> bool:
    """Check if URL is valid using regex
    """
    regex = re.compile(
        r'^(?:http|ftp)s?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    do_match = re.match(regex, url)

    if do_match:
        return True

    else:
        return False