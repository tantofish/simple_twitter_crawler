from twitwi.model.tweet import Tweet
from twitwi.model.uri import Uri
from bs4 import BeautifulSoup
import lxml
import re
import requests
import json

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
        self._session.headers.update({'User-Agent' : 'Mozilla/5.0'})
        self._res = ''
        self._soup = ''
        self._json = ''
        self.minTweetId = ''
        self.maxTweetId = ''
        self.positionCrumb = ''
        self._hasNextPage = True
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
        soup = BeautifulSoup(self._res.text,'lxml')
        self._soup = soup

        self.data_max_position = soup.select('.stream-container')[0].get('data-max-position')
        match = re.compile('^TWEET-(\d*)-(\d*)-(.*)$').match(self.data_max_position)
        self.minTweetId = match.group(1)
        self.maxTweetId = match.group(2)
        self.positionCrumb = match.group(3)

        self._ajaxUri.updateParams(self._uri.params)

        return self.parseTweets()

    def searchFromUrl(self, url):
        self._uri = Uri(url)
        return self._search()

    def searchFromQuery(self, query, tab='latest'):
        self._uri.updateParams({
            'q' : query,
            'f' : TwitterDao.tabMap.get(tab,''),
        })
        return self._search()

    def hasNextPage(self):
        return self._hasNextPage

    def getNextPage(self):
        max_position = 'TWEET-%s-%s-%s' % (self.minTweetId, self.maxTweetId, self.positionCrumb)
        self._ajaxUri.updateParams({'max_position' : max_position})
        self._res = self._session.get(self._ajaxUri.getUrl())

        self._json = json.loads(self._res.text)
        self._hasNextPage = self._json.get('has_more_items')
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

        self.minTweetId = str(min([int(t.tweetId) for t in tweetList]))

        return tweetList
