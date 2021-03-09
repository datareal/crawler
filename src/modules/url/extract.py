from __future__ import annotations

import tldextract
import urllib.parse

def extract_domain(url: str) -> Domain[str]:
    """Docstring for the _extract_domain function.

    Get the domain from a given url.

    Args:
        param1 (str) url:
            The url to get the domain from

    Returns:
        The domain from the url (str)
    """
    extractor: ClassVar[T]
    try:
        extractor = tldextract.TLDExtract(cache_file=False)

    except TypeError:
        extractor = tldextract.TLDExtract(cache_dir=False)

    extracted = extractor(url)

    domain: str = f'{extracted.domain}.{extracted.suffix}'

    return domain

def extract_path(url: str) -> Path[str]:
    """Docstring for the _extract_domain function.

    Get the domain from a given url.

    Args:
        param1 (str) url:
            The url to get the domain from

    Returns:
        The domain from the url (str)
    """
    extracted = urllib.parse.urlparse(url)

    path: str = extracted.path

    return path