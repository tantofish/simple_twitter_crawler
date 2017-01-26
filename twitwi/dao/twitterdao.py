from twitwi.model.tweet import Tweet
from twitwi.model.uri import Uri
from bs4 import BeautifulSoup
import lxml
import re
import requests
import json
import datetime

class TwitterDao:

    tabMap = {
        'top'   : '',
        'latest': 'tweets',
        'people': 'users',
        'photo' : 'images',
        'videos': 'videos',
        'periscopes': 'periscopes',
        'news'  : 'news'
    }
 
    def __init__(self, **kwargs):
        self._uri = Uri('https://twitter.com/search?') \
            .updateParams({
                'q'        : 'helloworld',
                'f'        : 'tweets',
                'vertical' : 'default',
                'src'      : 'typd',
            })
        self._ajaxUri = Uri('https://twitter.com/i/search/timeline?') \
            .updateParams({
                'q'                 : 'helloworld',
                'f'                 : 'tweets',
                'vertical'          : 'default',
                'src'               : 'typd',
                'reset_error_state' : 'false',
                'include_entities'  : '1',
                'include_available_features' : '1',
            })

        self._session = requests.Session()
        self._session.headers.update({'User-Agent' : '*'})
        self._res = ''
        self._soup = ''
        self._json = ''
        self._lang = ''
        self._since = ''
        self._until = ''
        self.minTweetId = ''
        self.maxTweetId = ''
        self.positionCrumb = ''
        self._hasNextPage = 2
        self._isFirstAjax = True
        self.__dict__.update(kwargs)

    def getUri(self):
        return self._uri

    def getAjaxUri(self):
        return self._ajaxUri

    def getResponse(self):
        return self._res

    def getMaxTweetId(self):
        return self.maxTweetId

    def getMinTweetId(self):
        return self.minTweetId

    def getPositionCrumb(self):
        return self.positionCrumb

    def _search(self):
        self._res = self._session.get(self._uri.getUrl())
        self._soup = BeautifulSoup(self._res.text,'lxml')

        self.data_max_position = self._soup.select('.stream-container')[0].get('data-max-position')
        match = re.compile('^TWEET-(\d*)-(\d*)-(.*)$').match(self.data_max_position)
        self.minTweetId = match.group(1)
        self.maxTweetId = match.group(2)
        self.positionCrumb = match.group(3)

        self._ajaxUri.updateParams(self._uri.params)

        self._isFirstAjax = True
        return self.parseTweets()

    def searchFromUrl(self, url):
        self._uri = Uri(url)
        return self._search()


    def search(self, query):
        fullQuery = query

        if self._lang:
            fullQuery += ' lang:' + self._lang
        if self._since:
            fullQuery += ' since:' + self._since.strftime('%Y-%m-%d')
        if self._until:
            fullQuery += ' until:' + self._until.strftime('%Y-%m-%d')

        self._uri.updateParams({'q' : fullQuery})
        return self._search()
    
    def tab(self, tab):
        self._uri.updateParams({'f' : TwitterDao.tabMap.get(tab,'')})
        return self

    def lang(self, lang):
        self._lang = lang
        return self

    def since(self, since):
        self._since = datetime.datetime.strptime(since,'%Y-%m-%d')
        return self

    def until(self, until):
        self._until = datetime.datetime.strptime(until,'%Y-%m-%d')
        if self._since and self._until <= self._since:
            raise Exception("'until' must be later than 'since'")
        return self

    def searchFromQuery(self, query, tab='latest'):
        self._uri.updateParams({
            'q' : query,
            'f' : TwitterDao.tabMap.get(tab,''),
        })
        return self._search()

    def hasNextPage(self):
        return self._hasNextPage

    def getNextPage(self):
        if self._isFirstAjax:
            max_position = self.data_max_position
            self._isFirstAjax = False
        else:
            max_position = 'TWEET-%s-%s-%s' % (self.minTweetId, self.maxTweetId, self.positionCrumb)

        self._ajaxUri.updateParams({'max_position' : max_position})
        self._res = self._session.get(self._ajaxUri.getUrl())


        self._json = json.loads(self._res.text)
        if self._json.get('has_more_items'):
            self._hasNextPage = 2
        else:
            self._hasNextPage -= 1
            print("hasNextPage returned as false, quota -= 1")
            print(self._ajaxUri.getUrl())

        #self._hasNextPage = self._json.get('has_more_items')

        self._soup = BeautifulSoup(self._json.get('items_html'), 'lxml')

        return self.parseTweets()

    def setParams(self, params):
        self._uri.updateParams(params)
        self._ajaxUri.updateParams(params)
        return self
    
    def parseTweet(self, soup):
        nLikeSelector = '.ProfileTweet-action--favorite .ProfileTweet-actionCount'
        nRetweetSelector = '.ProfileTweet-action--retweet .ProfileTweet-actionCount'
        tweet = Tweet(
            tweetId = soup.get('data-item-id'),
            content = soup.select_one('.tweet-text').text,
            author = soup.select_one('.fullname').text.split('\n')[0],
            authorId = soup.select_one('.username').text,
            timestamp = soup.select_one('._timestamp').get('data-time'),
            nLike = int(soup.select(nLikeSelector)[0].get('data-tweet-stat-count')),
            nRetweet = int(soup.select(nRetweetSelector)[0].get('data-tweet-stat-count'))
        )
        return tweet

    def parseTweets(self, html=None):
        if not html:
            soup = self._soup
        else:
            soup = BeautifulSoup(html,'lxml')
            self._soup = soup

        tweetElements = soup.select('li.stream-item div.tweet')
        tweetList     = [ self.parseTweet(t) for t in tweetElements ]

        if len(tweetList) > 0 :
            self.minTweetId = str(min([int(t.tweetId) for t in tweetList]))

        return tweetList
