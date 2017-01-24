from twitwi.model.tweet import Tweet
from twitwi.model.uri import Uri
from bs4 import BeautifulSoup
import requests
import json
import lxml
import sys
import csv
import re
import os

COL_GETTER_MAP = {
    'authorid'  : 'getAuthorId',
    'author'    : 'getAuthor',
    'time'      : 'getTime',
    'date'      : 'getDate',
    'tweetid'   : 'getTweetId',
    'timestamp' : 'getTimestamp',
    'content'   : 'getContent',
    'numlike'   : 'getNumLike',
    'numRetweet': 'getNumRetweet',
}

class CsvDao:
    def __init__(self, **kwargs):
        self.writePath = os.getcwd()
        self.filename = 'TwitwiCsvOutputExample.csv'
        self.targetColumns = []
        
        self.__dict__.update(kwargs)

        if (sys.version_info >= (3,0)):
            self.f = open(self.writePath + '/' + self.filename, 'w', encoding='utf-8')
        else:
            self.f = open(self.writePath + '/' + self.filename, 'w')
        self.csvWriter = csv.writer(self.f)

    def setTargetColumns(self, cols):
        self.targetColumns = cols
        return self

    def writeHeaders(self, headers=None):
        if not headers:
            headers = self.targetColumns

        self.csvWriter.writerow(headers)
        return self

    def writeTweet(self, tweet):
        def func_not_found(): # just in case we dont have the function
            raise ValueError("Can't find attribute getter \"" + func_name + "\" in Tweet")

        rowData = []
        for tc in self.targetColumns:
            func_name = COL_GETTER_MAP[tc.replace(" ","").lower()]
            getter = getattr(tweet, func_name, func_not_found)
            if (sys.version_info >= (3,0)):
                rowData.append(getter())
            else:
                rowData.append(getter().encode('utf-8'))

        self.csvWriter.writerow(rowData)

    def writeTweets(self, tweets):
        for t in tweets:
            self.writeTweet(t)

    def commit(self):
        self.f.close()
        print('File saved to : %s/%s' % (self.writePath, self.filename))
