
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

handles = [ 'NYTimes', 
            'NBCNews',
            'CBSNews',
            'Newsweek',
            'WashingtonPost',
            'Buzzfeed',
            'HuffPost',
            'CNN',
           
            'BBCWorld',
            'ProPublica',
            'AP',
            'WSJ',
            'NPR',
            
            'DailyMail',
            'NRO',
            'OANN',
            'BreitbartNews',
            'blazemedia',
            'FoxNews',]
tweets = []
for user in handles:
    tweetCriteria = got.manager.TweetCriteria().setQuerySearch('correction: from:' + user).setSince("2015-01-01")#.setMaxTweets(10)
    tweets.append([user, got.manager.TweetManager.getTweets(tweetCriteria)])


for tweet in tweets[1][1]:
    printTweet("tweet:", tweet)
    
dir(tweets[1][1][0])

print("Number of Correction Tweets by Organization:")
for tweet in tweets:
    print(tweet[0] + ": %d" %  len(tweet[1]))

avg_cor = []
for tweet in tweets:
    avg = 0
    for t in tweet[1]:
        avg += t.retweets
    avg = avg / len(tweets[0][1])
    avg_cor.append([tweet[0], avg])
    print (tweet[0] + " Average retweets for corrections: " + str(int(avg)))
   
tweets_nc = []
i = 0
for user in handles:
    if len(tweets[i][1]):
        tweetCriteria = got.manager.TweetCriteria().setUsername(user).setMaxTweets(len(tweets[i][1]))
        tweets_nc.append([user, got.manager.TweetManager.getTweets(tweetCriteria)])
    i += 1

avg_ncor = []
for tweet in tweets_nc:
    avg = 0
    for t in tweet[1]:
        avg += t.retweets
    avg = avg / len(tweets[0][1])
    avg_ncor.append([tweet[0], avg])
    print (tweet[0] + " Average retweets: " + str(int(avg)))
    
print("Percent Change from Normal to Corrected Retweets")
for i in range(0, len(avg_cor) -1):
    if avg_cor[i][1] != 0 :
        avg = (avg_cor[i][1] - avg_ncor[i][1]) / avg_cor[i][1]
        print(handles[i] + ": " + str(avg))
    else:
        print(handles[i] + ": " + str(0))