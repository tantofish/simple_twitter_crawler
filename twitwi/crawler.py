import os
import sys
import time
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from twitwi.dao.twitterdao import TwitterDao
from twitwi.dao.filedao    import CsvDao

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

class TwitterCrawler:
    def __init__(self, **kwargs):
        self.init()
        self.__dict__.update(kwargs)

    def init(self):
        # default attributes ( can be altered by member functions)
        today    = datetime.utcnow().date()
        tomorrow = today + timedelta(1) 
        self._since    = today.strftime('%Y-%m-%d')     # default utc today
        self._until    = tomorrow.strftime('%Y-%m-%d')  # default utc tomorrow
        self._filepath = os.getcwd()                    # where to save the csv file(s)
        self._filename = 'TwitwiOutput.csv'             # filename
        self._tab      = 'latest'                       # top, latest, people, videos, news, photo
        self._lang     = 'en'                           # language
        self._query    = '@upshelp'                     # name of the target timeline
        self._nTweets  = 0
        self._targetColumns = ['Author ID','Date','Time','Content']
        return self

    def since(self, since):
        self._since = since
        return self

    def until(self, until):
        self._until = until
        return self

    def setTargetColumns(self, targetColumns):
        self._targetColumns = targetColumns
        return self

    def saveTo(self, filepath):
        self._filepath = filepath
        return self

    def saveAs(self, filename):
        self._filename = filename
        return self

    def tab(self, tab):
        self._tab = tab
        return self

    def lang(self, lang):
        self._lang = lang
        return self

    def target(self, query):
        self._query = query
        return self

    def _saveTweets(self, tweets):
        if len(tweets) == 0:
            print('"tweets" list is empty. Nothing to write.')
            return 0

        self._nTweets += len(tweets)
        self.csvDao.writeTweets(tweets)
        
        lastRecordDate = tweets[-1].getDate()
        lastRecordTime = tweets[-1].getTime()
        print '\r  Accumulated Tweets: %d. Lastest Record Datetime: %s %s' % \
        (
            self._nTweets,
            lastRecordDate,
            lastRecordTime
        ),

        print "\r\r",
        sys.stdout.flush()

        return 1

    def go(self):

        dao = TwitterDao() \
                .tab(self._tab) \
                .lang(self._lang) \
                .since(self._since) \
                .until(self._until)

        self.nTweets = 0
        tweets = dao.search(self._query)

        if (len(tweets) > 0):
            print('=============== Start crawling!!! ===============')
            print('  target: %s' % self._query)
            print('  tab   : %s' % self._tab)
            print('  lang  : %s' % self._lang)
            print('  date  : from %s to %s' % (self._since, self._until))
            print('')

            # initial csv dao (file pointer and csv writer)
            self.csvDao = CsvDao(writePath=self._filepath, filename=self._filename) \
                            .setTargetColumns(self._targetColumns) \
                            .writeHeaders()

            while len(tweets) > 0:
                time.sleep(0.8)
                self._saveTweets(tweets)
                tweets = dao.getNextPage()

            print('')
            print('')
            self.csvDao.commit()
        else:
            print('=============== No Records Found ===============')
            print('  target: %s' % self._query)
            print('  tab   : %s' % self._tab)
            print('  lang  : %s' % self._lang)
            print('  date  : from %s to %s' % (self._since, self._until))
            print('')

        return self



# example 1 crawl one month into 1 file
def example1():
    crawler = TwitterCrawler()
    crawler.init() \
           .since('2015-01-01') \
           .until('2015-02-01') \
           .setTargetColumns(['Author ID', 'Date', 'Time', 'Content']) \
           .target('@fedexhelp') \
           .lang('en') \
           .tab('latest') \
           .saveAs('Fedex-2015-01.csv') \
           .go()



# example 2 crawl one year into 12 files
def example2():
    start_date = date(2015,1,1)     # the start date for crawl
    nMonth     = 24                 # n month to crawl

    print("Hello! We are going to crawler the following sets of data:")
    print("")
    for i in range(0,nMonth):
        since = start_date + relativedelta(months=i)
        month = since.month
        year  = since.year
        until = start_date + relativedelta(months=i+1)
        since = since.strftime('%Y-%m-%d')
        until = until.strftime('%Y-%m-%d')
        filename = 'FEDEX_%4d-%02d.csv' % (year, month)
        print("    %2d. since: %s, until: %s, save as: %s" % ((i+1), since, until, filename))

    print("")
    time.sleep(0.5)
    print("Starts in 1 second.")
    time.sleep(1.0)
    print("Here we go!!")
    print("")
        
    for i in range(0,nMonth):
        since = start_date + relativedelta(months=i)
        month = since.month
        year  = since.year
        until = start_date + relativedelta(months=i+1)
        since = since.strftime('%Y-%m-%d')
        until = until.strftime('%Y-%m-%d')
        filename = 'FEDEX_%4d-%02d.csv' % (year, month)

        crawler = TwitterCrawler()
        crawler.init() \
               .since(since) \
               .until(until) \
               .setTargetColumns(['Author ID', 'Date', 'Time', 'Content']) \
               .target('@fedexhelp') \
               .lang('en') \
               .tab('latest') \
               .saveAs(filename) \
               .go()


if __name__ == '__main__':
    example2()
