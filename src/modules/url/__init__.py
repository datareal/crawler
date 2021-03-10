from urllib.parse import urljoin
from w3lib.url import safe_url_string

from .extract import extract_domain, extract_path
from .validate import escape_ajax, validator