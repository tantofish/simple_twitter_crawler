import time
import datetime
from twitwi.dao.twitterdao import TwitterDao
from twitwi.dao.filedao    import CsvDao
import os

def crawl(
        query,
        targetDate = datetime.date.today().strftime('%Y-%m-%d'),
        filename = 'TwitwiOutput.csv',
        filepath = os.getcwd()
    ):


    def saveTweets(tweets, nTweets):
        if not len(tweets):
            return lastRecordDate, nTweets 

        trueLastRecordDate = tweets[-1].getDate()
        tweets = [t for t in tweets if t.getDate() == targetDate]
        if len(tweets) > 1:
            nTweets += len(tweets)
            tDate = tweets[-1].getDate()
            tTime = tweets[-1].getTime()
            csvDao.writeTweets(tweets)
            print('Accumulated tweets: %d. Last record date,time: %s %s' % (nTweets, tDate, tTime))
        else:
            print('To the end.')

        time.sleep(0.8)
        return trueLastRecordDate, nTweets
   
    dao = TwitterDao().tab('latest').lang('en')
    csvDao = CsvDao(writePath=filepath, filename=filename) \
               .setTargetColumns(['Author ID','Content','Time','Date']) \
               .writeHeaders()

    tweets = dao.until(targetDate).search(query)
    lastRecordDate, nTweets = saveTweets(tweets, 0)

    while dao.hasNextPage() and targetDate == lastRecordDate:
        tweets = dao.getNextPage()
        lastRecordDate, nTweets = saveTweets(tweets, nTweets)

    csvDao.commit()


if __name__ == '__main__':
    today = datetime.date.today().strftime('%Y-%m-%d')
    crawl('@upshelp', today)
