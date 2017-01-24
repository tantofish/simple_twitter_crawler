import time
import datetime
from twitwi.dao.twitterdao import TwitterDao
from twitwi.dao.filedao    import CsvDao
import os

#class TwitterCrawler:
#
#    def __init__(self):
#        twiDao = TwitterDao().tab('latest').lang('en')
#        csvDao = CsvDao(writePath='', filename='TwitwiOutput.csv') \
#                   .setTargetColumns(['Author ID','Content','Time','Date']) \
#                   .writeHeaders()
#    
#    def crawl(self, query, since = None, until = None):




def crawl(
        query,
        date = datetime.date.today().strftime('%Y-%m-%d'),
        filename = 'TwitwiOutput.csv',
        filepath = os.getcwd()
    ):
    dao = TwitterDao().tab('latest').lang('en')
    tweets = dao.until(date).search(query)

    csvDao = CsvDao(writePath=filepath, filename=filename) \
               .setTargetColumns(['Author ID','Content','Time','Date']) \
               .writeHeaders()

    csvDao.writeTweets(tweets)

    nTweets = len(tweets)
    tDate = tweets[-1].getDate()
    tTime = tweets[-1].getTime()
    print('accumulated tweets: %d, last record datetime: %s %s' % (nTweets, tDate, tTime))
    time.sleep(0.5)
    
    while dao.hasNextPage() and date == tDate:
        tweets = dao.getNextPage()
        csvDao.writeTweets(tweets)
        nTweets += len(tweets)
        tDate = tweets[-1].getDate()
        tTime = tweets[-1].getTime()
        print('accumulated tweets: %d, last record datetime: %s %s' % (nTweets, tDate, tTime))
        time.sleep(0.5)

    csvDao.commit()


if __name__ == '__main__':
    today = datetime.date.today().strftime('%Y-%m-%d')
    crawl('@upshelp', today)
