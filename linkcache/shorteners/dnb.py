#!/usr/bin/env python
# -*- coding: utf-8 -*-,

import re
import common
import linkcache.browser
import urllib


selfRefRegex = re.compile(r"http://dnb.us/([A-Za-z0-9]+)")
class DnbShortener(common.GenericShortener):
    apiurl = 'http://dnb.us/surl-api.php?url=%s'
    def __init__(self, config):
        common.GenericShortener.__init__(self, config)
        self.browser = linkcache.browser.SingletonBrowser()

    def self_reference(self, url):
        return selfRefRegex.search(url) is not None

    def pre_shorten(self, url):
        url = urllib.quote(url)
        r = self.browser.open(self.apiurl % url)
        dnburl = r.text.strip()
        return dnburl

instantiate = DnbShortener

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
