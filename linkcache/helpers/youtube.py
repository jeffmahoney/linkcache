#!/usr/bin/env python
# -*- coding: utf-8 -*-,

from common import UrlHelper
from urlparse import urlparse, parse_qs
import re
import string
import urllib2
from bs4 import BeautifulSoup

class YoutubeHelper(UrlHelper):
    def __init__(self, config):
        UrlHelper.__init__(self, config)
        self.clear_title = False
        self.provides = [ 'title', 'url' ]

        domains = [ 'youtube\.com', 'youtu\.be' ]

        self.url_regex = re.compile("(" + string.join(domains,"|") + ")/.*")

    def fetch(self, browser, url):
        targetUrl = url

        pURL = urlparse(url)
        query = parse_qs(pURL.query)

        params = ""
        titleCharms = ""

        if 't' in query:
            params += "#t=" + str(query['t'][0])
            titleCharms += " [timecode]"

        if pURL.fragment and (pURL.fragment.find("t=") > -1):
            params += "#" + pURL.fragment
            titleCharms += " [timecode]"

        if 'list' in query:
            params += "&list=" + str(query['list'][0])
            titleCharms += " [playlist]"

        if 'youtu.be' in pURL.netloc:
            targetUrl = "https://www.youtube.com/watch?v=" + pURL.path[1:]
            targetUrl += params
        elif 'v' in query:
            targetUrl = "https://www.youtube.com/watch?v=" + str(query['v'][0])
            targetUrl += params
        else:
            targetUrl = url
            targetUrl = re.sub("^https", "http", url)

        target = urllib2.urlopen(targetUrl)

        sO = BeautifulSoup(target.read())

        title = sO.title.string + titleCharms

        return {'title': title, 'url': targetUrl }
instantiate = YoutubeHelper
# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
