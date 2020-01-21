import tweepy
import sys
import unicodecsv as csv

## please enter your credentials here
consumer_key = "eUed9xOxK2WXmrGoC5YYONnrI"
consumer_secret = "lQJHgwt3mxUFRvyfzpxoYCeV1itPv0aVaC7GRjqJ52NuqUHlJZ"
access_token = "767679563514208260-3k1PuvqHDe05BA8URfTxX8mGu5ERY8N"
access_token_secret = "EGmghjfCjLHvWdhjvBaLxZGMMjFjY5xFOvQrCCIdq2jwo"


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify=True)

readfile = sys.argv[1]
writefile = sys.argv[2]

with open (readfile, "rb") as rf:
    with open (writefile, "wb") as wf:
        tsvwriter = csv.writer(wf, delimiter = "\t")

        tweet_id = rf.readline()
        while tweet_id:
            try:
                tweet_id = tweet_id.strip()
                tweet = api.get_status(tweet_id)
                tweet = tweet.fulltext
            except:
                tweet = ""

            tweet = tweet.replace("\t", " TAB ")
            tweet = tweet.replace("\n", " NEWLINE " )
            tweet = tweet.replace("\r\n", " NEWLINE " )
            tweet_id = tweet_id.decode("UTF-8")

            tsvwriter.writerow([tweet_id,tweet])
            tweet_id = rf.readline()



