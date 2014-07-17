#!/usr/bin/env python
# -*- coding: utf-8 -*-,

from common import UrlHelper
from bs4 import BeautifulSoup
import re
import urllib2

class ReadabilityHelper(UrlHelper):
    def __init__(self, config):
        UrlHelper.__init__(self, config)
        self.clear_title = True
        self.url_regex = re.compile("readability.com/articles/.*")
        self.provides = [ 'title', 'url' ]

    def fetch(self, browser, url):
        url = re.sub("/#!", "", url)
        url = re.sub("^https", "http", url)
        resp = browser.open(url)
        html = resp.read()
        s = BeautifulSoup(html)

        return {'title': s.title.string.strip(), 'url': resp.geturl() }

instantiate = ReadabilityHelper
# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
