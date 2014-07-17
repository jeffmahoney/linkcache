#!/usr/bin/env python
# -*- coding: utf-8 -*-,

from common import UrlHelper
import twitter
import re

class TwitterHelper(UrlHelper):
    config_section = 'twitter'

    def __init__(self, config):
        UrlHelper.__init__(self, config)

        self.provides = [ 'description' ]
        self.clear_title = True
        self.url_regex = re.compile("twitter.com.*status")

        self.twitterApi = twitter.Api(
            consumer_key=config['consumer_key'],
            consumer_secret=config['consumer_secret'],
            access_token_key=config['access_token_key'],
            access_token_secret=config['access_token_secret'])

    def fetch(self, browser, url):
        url = re.sub("/#!", "", url)
        url = re.sub("^https", "http", url)
        url = re.sub("/photo/.*", "", url)

        regex = re.compile(r".*twitter.com.*status[es]*/(\d+)")
        tweet_id = regex.search(url).group(1)

        try:
            tweet = self.twitterApi.GetStatus(id=tweet_id)
            tweet_desc = "@" + tweet.user.screen_name + ": " + tweet.text
            return {'description': tweet_desc}
        except twitter.TwitterError, e:
            return None

instantiate = TwitterHelper
# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
