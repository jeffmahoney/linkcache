#!/usr/bin/env python
# -*- coding: utf-8 -*-,

from common import UrlHelper
from bs4 import BeautifulSoup
import re

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
        s = BeautifulSoup(resp.text)

        return {'title': s.title.string.strip(), 'url': resp.url }

instantiate = ReadabilityHelper
# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
