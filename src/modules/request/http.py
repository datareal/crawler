import requests

import src.modules.url as URL
import src.modules.errors as errors
import src.modules.exceptions as exceptions

class Request:
    """
    A simple object-oriented http request library.

    A request[GET, POST] is made when passed a url, creating a random header object
    and also rendering with Splash (see https://github.com/scrapinghub/splash).
    """
    def __init__(
        self,
        url: str,
        *,
        method: str = 'GET',
        header: dict = dict(),
        encoding: str = 'UTF-8',
        render: bool = False
    ) -> None:
        """
        Creates the Request objcet.

        Args:
            param1 (str) url:
                String containing the target url to make the HTTP request
                Can't be none
            param2 (str) method:
                String containing which Request method we will perform
                Must be one of the followings:
                - GET
            param3 (dict) header:
                Dict containing all needed headers for the request
                If none it will generate a random header
            param4 (str) encoding:
                String containing which character encoding will be used
                Can't be none but can be empty
            param5 (bool) render:
                Boolean variable that describes if the website needs to be rendered or not    
        """
        self.method = str(method).upper()
        self.encoding = str(encoding).upper()
        self.render = render
        self.header = header

        if not bool(header):
            self.header = {}
            
        self._set_url(url)
        self._set_session()

    def _set_url(self, url):
        if not isinstance(url, str):
            raise TypeError(f'Request url must be str or unicode, got {type(url).__name__}')

        safe_url = URL.safe_url_string(url, self.encoding)
        self._url = URL.escape_ajax(safe_url)

        if ('://' not in self._url) and (not self._url.startswith('data:')):
            raise ValueError(f'Missing scheme in request url: {self._url}')

    def _set_session(self):
        request_args = dict()

        if bool(self.render):
            request_args['url'] = self._url

            # We need to create the Splash Docker container in AWS to be able to render it 
            #
            # params = {
            #     'wait': 0.5,
            #     'timeout': 10,
            #     'url': self._url
            # }

            # request_args['url'] = 'http://localhost:8050/render.html?'
            # request_args['params'] = params

        else:
            request_args['url'] = self._url 

        request: ClassVar = requests.Request(
            headers=self.header,
            method=self.method,
            **request_args
        )

        self.prepared_request = request.prepare()
        self.session = requests.Session()

    def fetch(self):
        response = self.session.send(self.prepared_request)

        if response.ok:
            return response

        else:
            if response.status_code == 403:
                errors.forbbiden(self._url)
                raise exceptions.RequestForbbiden(f"The requested url {self._url} returned a 403 status code.")

            return response