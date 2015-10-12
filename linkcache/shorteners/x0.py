#!/usr/bin/env python
# -*- coding: utf-8 -*-,

import re
import common
import linkcache.browser
import urllib


selfRefRegex = re.compile(r"https://x0.no/([A-Za-z0-9]+)")
class x0Shortener(common.GenericShortener):
    apiurl = 'https://x0.no/api/?%s'
    def __init__(self, config):
        common.GenericShortener.__init__(self, config)
        self.browser = linkcache.browser.Browser()

    def self_reference(self, url):
        return selfRefRegex.search(url) is not None

    def pre_shorten(self, url):
        r = self.browser.open(self.apiurl % url)
        x0url = r.text.strip()
        return x0url

instantiate = x0Shortener

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
