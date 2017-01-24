# simple_twitter_crawler
Just a practice of crawling (ongoing, not completed yet)

## How to install
```bash
git clone git@github.com:tantofish/simple_twitter_crawler.git
cd simple_twitter_crawler
python setup.py install
```

## How to Use
### simple demo
```python
from twitwi.crawler import crawl
crawl('@upshelp', '2017-01-23', 'TestFilename.csv')
```

### use the DAOs
```python
import time
from twitwi.dao.twitterdao import TwitterDao
from twitwi.dao.filedao    import CsvDao

dao = TwitterDao().tab('latest').lang('en')
tweets = dao.since('2017-01-03').until('2017-01-04').search('@UPShelp')

csvDao = CsvDao(writePath='/Users/yutu/Desktop/', filename='TwitwiOutput.csv') \
           .setTargetColumns(['Author ID','Content','Time','Date']) \
           .writeHeaders()

csvDao.writeTweets(tweets)

nTweets = len(tweets)

while dao.hasNextPage():
    tweets = dao.getNextPage()
    csvDao.writeTweets(tweets)
    nTweets += len(tweets)
    tDate = tweets[-1].getDate()
    tTime = tweets[-1].getTime()
    print('accumulated tweets: %d, last record datetime: %s %s' % (nTweets, tDate, tTime))
    time.sleep(0.5)

csvDao.commit()
```

