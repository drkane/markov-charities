import random
import json
import os
import time
import tweepy
import configargparse
import gzip
from datetime import datetime
from file_markov import FileMarkov

# connect to twitter API and tweet
# from: https://videlais.com/2015/03/02/how-to-create-a-basic-twitterbot-in-python/
class TwitterAPI:
    def __init__(self, cfg):
        auth = tweepy.OAuthHandler(cfg["consumer_key"], cfg["consumer_secret"] )
        auth.set_access_token(cfg["access_token"], cfg["access_token_secret"])
        self.api = tweepy.API(auth)

    def tweet(self, message):
        self.api.update_status(status=message)

if __name__ == "__main__":
    
    p = configargparse.ArgParser(ignore_unknown_config_file_keys=True)
    p.add('-c', '--my-config', default="example.cfg", is_config_file=True, help='config file path')
    
    # Twitter connection details
    p.add('--consumer-key', help='Twitter authorisation: consumer key')
    p.add('--consumer-secret', help='Twitter authorisation: consumer secret')
    p.add('--access-token', help='Twitter authorisation: access token')
    p.add('--access-token-secret', help='Twitter authorisation: access token secret')
    
    # Time to sleep between tweets (in seconds - default is one hour)
    p.add('-s', '--sleep', default=3600, type=int, help='Time to sleep between tweets (in seconds - default is one hour)')
    
    # filename of charity data file
    p.add("-f", "--file", default="charities.csv.gz", help="Location of charity data file")
    
    p.add("--debug", action='store_true', help="Debug mode (doesn't actually tweet)")

    options = p.parse_args()
    
    # set up markov chain
    m = FileMarkov( options.file )
    
    # connect to Twitter API
    twitter = TwitterAPI(vars(options))
    print("Connected to twitter. User: [{}]".format( twitter.api.me().screen_name ) )
    if options.debug:
        print("[DEBUG] Not actually tweeting every {} seconds".format( options.sleep ))
    else:
        print("Tweeting every {} seconds".format( options.sleep ))
    
    while True:
        tweet = m.get_tweet()
        if not options.debug:
            twitter.tweet(tweet)
        print("{:%Y-%m-%d %H:%M:%S}: {tweet}".format(datetime.now(), tweet=tweet) )
        time.sleep(options.sleep)


