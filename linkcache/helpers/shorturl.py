#!/usr/bin/env python
# -*- coding: utf-8 -*-,

from common import UrlHelper
import re
import string
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

        target = browser.open(url)
        targeturl = target.url

        sO = BeautifulSoup(target.text)

        return {'title': sO.title.string, 'url': targeturl }

instantiate = ShortUrlHelper
# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
