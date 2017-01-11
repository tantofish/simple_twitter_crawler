from twitwi.model.tweet import Tweet
from bs4 import BeautifulSoup
import lxml
import re

class TwitterDao:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

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

    def parseTweets(self, html):
        soup = BeautifulSoup(html,'lxml')
        tweets = soup.select('li.stream-item div.tweet')
        nTweets = [ self.parseTweet(t) for t in tweets ]
        return nTweets
