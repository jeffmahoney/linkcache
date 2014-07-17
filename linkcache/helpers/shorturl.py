#!/usr/bin/env python
# -*- coding: utf-8 -*-,

from common import UrlHelper
import re
import string
import urllib2
from bs4 import BeautifulSoup

class ShortUrlHelper(UrlHelper):
    def __init__(self, config):
        UrlHelper.__init__(self, config)
        self.clear_title = True
        self.provides = [ 'title', 'url' ]

        domains = [ "bit\.ly",   # Bitly
                    "goo\.gl",   # Google
                    "kck\.st",   # Kickstarter
                    "sbn\.to"    # SBNation
                  ];

        self.url_regex = re.compile("(" + string.join(domains,"|") + ")/.*")

    def fetch(self, browser, url):
        url = re.sub("/#!", "", url)
        url = re.sub("^https", "http", url)

        target = urllib2.urlopen(url)
        targeturl = target.geturl()

        sO = BeautifulSoup(target.read())

        return {'title': sO.title.string, 'url': targeturl }

instantiate = ShortUrlHelper
# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
