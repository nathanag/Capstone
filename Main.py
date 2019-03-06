
#pip install pyquery

import sys
if sys.version_info[0] < 3:
    import got
else:
    import got3 as got

def printTweet(descr, t):
	print(descr)
	print("Username: %s" % t.username)
	print("Retweets: %d" % t.retweets)
	print("Text: %s" % t.text)
	print("Mentions: %s" % t.mentions)
	print("Hashtags: %s\n" % t.hashtags)

handles = ['NYTimes', 
            'NBCNews',
            'ProPublica',
            'FoxNews',
            'CBSNews'
            'Newsweek',
            'WashingtonPost',
            'Buzzfeed',
            'HuffPost',
            'BreitbartNews',
            'CNN',
            'BBC',
            'AP',
            'WSJ',
            'NPR',]
tweets = []
for user in handles:
    tweetCriteria = got.manager.TweetCriteria().setQuerySearch('correction from:' + user).setSince("2015-05-01")#.setMaxTweets(10)
    tweets.append([user, got.manager.TweetManager.getTweets(tweetCriteria)])


for tweet in tweets[1][1]:
    printTweet("tweet:", tweet)

