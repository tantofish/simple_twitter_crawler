import os
import sys
import time
import datetime
from datetime import date, timedelta
from twitwi.dao.twitterdao import TwitterDao
from twitwi.dao.filedao    import CsvDao

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days) + 1):
        yield start_date + timedelta(n)

class TwitterCrawler:
    def __init__(self, **kwargs):
        # default attributes ( can be altered by member functions)
        self.filepath = os.getcwd()             # where to save the csv file(s)
        self.filepref = 'UPS'                   # filename prefix which will followed by the target date
        self.filename = 'TwitwiOutput.csv'      # filename
        self._since   = datetime.date.today()   # start date  (date object)
        self._until    = self._since              # end date    (date object)
        self._targetDate = self._since.strftime('%Y-%m-%d') # target date (str object)
        self._tab      = 'latest'                # top, latest, people, videos, news, photo
        self._lang     = 'en'                    # language
        self._query    = '@upshelp'              # name of the target timeline
        self.nTweets  = 0
        self.lastRecordDate = ''
        self.trueLastRecordDate = ''
        self.__dict__.update(kwargs)


    def _filterTweets(self, tweets):
        # get the date of the true last record
        self.trueLastRecordDate = tweets[-1].getDate()

        # filter out those records that is not in the target date
        tweets = [t for t in tweets if t.getDate() == self._targetDate]

        return tweets

    def _saveTweets(self, tweets):
        if len(tweets) == 0:
            print('len(tweets) == 0, nothing to write.')
            return 0
        elif len(tweets) >= 1:
            self.nTweets += len(tweets)
            self.csvDao.writeTweets(tweets)
            self.lastRecordDate = tweets[-1].getDate()
            self.lastRecordTime = tweets[-1].getTime()
            print('Accumulated tweets: %d. Last record date,time: %s %s' % (
                self.nTweets,
                self.lastRecordDate,
                self.lastRecordTime)
            )
        else:
            raise Exception('unexpected len(tweets): %d' % len(tweets))

        return 1


    def since(self, since):
        self._since = datetime.datetime.strptime(since, '%Y-%m-%d').date()
        return self

    def until(self, until):
        self._until = datetime.datetime.strptime(until, '%Y-%m-%d').date()
        return self

    def _setTargetDate(self, date):
        self._targetDate = date
        return self

    def _setFileName(self, filename):
        self.filename = filename
        return self

    def saveTo(self, filepath):
        self.filepath = filepath
        return self

    def saveAs(self, filepref):
        self.filepref = filepref
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

    def go(self):
        for d in daterange(self._since, self._until):
            dateStr = d.strftime("%Y-%m-%d")
            filePre = self.filepref

            self._setTargetDate(dateStr) \
                ._setFileName("%s_%s.csv" % (filePre, dateStr)) \
                ._crawl()

        return self

    def _crawl(self):

        dao = TwitterDao().tab(self._tab).lang(self._lang).until(self._targetDate)

        tweets = dao.search(self._query)
        tweets = self._filterTweets(tweets)

        if (len(tweets) > 0):
            print('======== Start crawling!!! ========')
            print('  target: %s' % self._query)
            print('  tab   : %s' % self._tab)
            print('  lang  : %s' % self._lang)
            print('  date  : %s' % self._targetDate)

            self.csvDao = CsvDao(writePath=self.filepath, filename=self.filename) \
                            .setTargetColumns(['Author ID','Content','Time','Date']) \
                            .writeHeaders()

            self._saveTweets(tweets)

            while dao.hasNextPage() and self._targetDate == self.trueLastRecordDate:
                time.sleep(0.8)
                tweets = dao.getNextPage()
                tweets = self._filterTweets(tweets)
                if len(tweets) == 0:
                    break

                self._saveTweets(tweets)

            print()
            self.csvDao.commit()
        else:
            print('======== No records in date: %s ========' % self._targetDate)

        return self


if __name__ == '__main__':
    crawler = TwitterCrawler()
    crawler.since('2015-01-01') \
           .until('2016-02-01') \
           .target('@fedexhelp') \
           .lang('en') \
           .tab('latest') \
           .saveTo('/Users/yutu/Desktop/twitter') \
           .saveAs('Fedex') \
           .go()
