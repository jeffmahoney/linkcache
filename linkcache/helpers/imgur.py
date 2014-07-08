#!/usr/bin/env python

from common import UrlHelper
import re
from bs4 import BeautifulSoup

class ImgurHelper(UrlHelper):
    def __init__(self, config):
        UrlHelper.__init__(self, config)
        self.clear_title = True
        self.url_regex = re.compile("imgur.com/(\S+)\....")
        self.provides = [ 'title' ]

    def match(self, url):
        return self.url_regex.search(url) is not None

    def fetch(self, browser, url):
        m = self.url_regex.search(url)
        url = "http://imgur.com/gallery/%s" % (m.group(1))

        r = browser.open(url)
        s = BeautifulSoup(r.read())

        title = s.title.string
        if title is not None:
            title = " ".join(title.split())

        return { 'title' : title }

instantiate = ImgurHelper

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
