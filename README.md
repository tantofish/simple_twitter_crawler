# simple_twitter_crawler
Just a practice of crawling (ongoing, not completed yet)

## How to install
```bash
git clone git@github.com:tantofish/simple_twitter_crawler.git
cd simple_twitter_crawler
python setup.py install
```

## How to Use
```python
>>> import requests
>>> iRes = requests.get("https://twitter.com/search?f=tweets&vertical=default&q=%40upshelp&src=typd")
>>>
>>> from twitwi.dao.twitterdao import TwitterDao
>>> td = TwitterDao()
>>> tweets = td.parseTweets(iRes.text)
>>>
>>> t1 = tweets[0]
>>> t1.
t1.author          t1.getAuthor(      t1.getDate(        t1.getNumRetweet(  t1.getTimestamp(   t1.nLike           t1.setAuthor(      t1.setNumLike(     t1.setTimestamp(   t1.timestamp       t1.tweetId
t1.content         t1.getContent(     t1.getNumLike(     t1.getTime(        t1.getTweetId(     t1.nRetweet        t1.setContent(     t1.setNumRetweet(  t1.setTweetId(     t1.toString(
>>> t1.author
'Karthik Rudra Shiva'
>>> t1.content
"@UPSHelp 1Z1A48T96713999585\nIt's a shame u have the worst team in Bangalore, or the worst service u provide 2days now held in wearhouse? ??"
>>> print(t1.toString())
=========== Tweet ID: 819219070335811584 ===========
  Author: Karthik Rudra Shiva
  Date: 2017-01-12
  Time: 00:27:01
  Content: @UPSHelp 1Z1A48T96713999585
It's a shame u have the worst team in Bangalore, or the worst service u provide 2days now held in wearhouse? ??
  Num of Likes: 0
  Num of Retweets: 0
```

