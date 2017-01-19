class Uri:
    def __init__(self, url = None):
        if url is None:
            self.scheme = ''
            self.hostname = ''
            self.params = {}
            self.path = ''
            self.port = ''
            self.query = ''
        else:
            self.setUrl(url)

    @staticmethod
    def query2dict(query):
        if not query:
            return {}

        if(query[0] == '?'):
            query = query[1:]

        if(query[-1] == '&'):
            query = query[0:-1]

        return { x.split('=')[0]:x.split('=')[1] for x in query.split('&') if len(x.split('=')) == 2 }

    def setUrl(self, url):
        # scheme
        s = url.split('://')
        if len(s) is 1:
            self.scheme = 'http'
            s = s[0]
        elif len(s) is 2:
            self.scheme = s[0]
            s = s[1]
        else:
            raise ValueError('parse url scheme fail, url: %s' % url)

        # params
        s = s.split('?')
        if len(s) is 1:
            # no param
            self.query  = ''
            self.params = {}
        elif len(s) is 2:
            # has params
            self.query    = s[1].split('#')[0]
            self.params   = Uri.query2dict(self.query)
        else:
            raise ValueError('parse url params fail, url: %s' % url)

        s = s[0].split('/',1)
        if len(s) is 1:
            # no path
            self.path = ''
        elif len(s) is 2:
            # has path
            self.path = s[1]
        else:
            raise ValueError('parse url path fail, url: %s' % url)

        s = s[0].split(':')

        self.hostname = s[0]
        self.port     = '' if len(s) is 1 else int(s[1])

        
        return self

    def getUrl(self):
        url = "%s://%s" % (self.scheme, self.hostname)

        if self.port:
            url += ':%s' % str(self.port)
        if self.path:
            url += '/%s' % self.path
        if self.params:
            url += "?%s" % self.genQuery()

        return url

    def genQuery(self):
        query = ''
        for k,v in self.params.items():
            query += "%s=%s&" % (k, str(v))
        return query[:-1]

    def updateParams(self, params):
        self.params.update(params)
        return self
