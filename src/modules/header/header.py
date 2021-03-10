from .fake_useragent import UserAgent

class Header(object):
    def __init__(self, header = dict()):
        if header is None:
            header = dict()
        self.headers = header

        self.__get_header__()
        
    def __get_header__(self):
        if not 'user-agent' in self.headers:
            user_agent = UserAgent().random()
            self.headers.update({'User-Agent': user_agent})

        self.headers.update({'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'})
        self.headers.update({'Accept-Language': 'en-US,en;q=0.9,pt;q=0.8'})
        self.headers.update({'Cache-Control': 'no-cache'})
        self.headers.update({'Connection': 'keep-alive'})
        self.headers.update({'Pragma': 'no-cache'})
        self.headers.update({'Sec-Fetch-Dest': 'document'})
        self.headers.update({'Sec-Fetch-Mode': 'navigate'})
        self.headers.update({'Sec-Fetch-Site': 'same-origin'})

        return self.headers
