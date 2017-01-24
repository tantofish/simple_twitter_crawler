from datetime import datetime

class Tweet:
    def __init__(self, **kwargs):
        self.timestamp = ""
        self.content = ""
        self.author = ""
        self.author = ""
        self.nLike = ""
        self.nRetweet = ""
        self.tweetId = ""
        self.__dict__.update(kwargs)
    
    def setTimestamp(self, ts):
        self.timestamp = ts

    def getTimestamp(self):
        return self.timestamp

    def getTime(self):
        return datetime.fromtimestamp(int(self.timestamp)) \
                       .strftime('%H:%M:%S')

    def getDate(self):
        return datetime.fromtimestamp(int(self.timestamp)) \
                       .strftime('%Y-%m-%d')

    def setContent(self, content):
        self.content = content

    def getContent(self):
        return self.content

    def setAuthor(self, author):
        self.author = author

    def getAuthor(self):
        return self.author

    def setAuthorId(self, authorId):
        self.authorId = authorId

    def getAuthorId(self):
        return self.authorId

    def setNumLike(self, nLike):
        self.nLike = nLike

    def getNumLike(self):
        return self.nLike
    
    def setNumRetweet(self, nRetweet):
        self.nRetweet = nRetweet

    def getNumRetweet(self):
        return self.nRetweet

    def setTweetId(self, tweetId):
        self.tweetId = tweetId
        
    def getTweetId(self):
        return self.tweetId

    def toString(self):
        return "=========== Tweet ID: " + self.tweetId + " ===========\n" + \
               "  Author: " + self.author + "\n" + \
               "  Author ID: " + self.author_id + "\n" \
               "  Date: " + self.getDate() + "\n" + \
               "  Time: " + self.getTime() + "\n" + \
               "  Content: " + self.content + "\n" + \
               "  Num of Likes: " + str(self.nLike) + "\n" + \
               "  Num of Retweets: " + str(self.nRetweet) + "\n"
