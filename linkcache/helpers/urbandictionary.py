#!/usr/bin/env python
# -*- coding: utf-8 -*-,

from common import UrlHelper
import re
from bs4 import BeautifulSoup

class UrbanDictionaryHelper(UrlHelper):
    def __init__(self, config):
        UrlHelper.__init__(self, config)
        self.clear_title = True
        self.url_regex = re.compile(".*urbandictionary.com/define.php.*")
        self.provides = [ 'title', 'description' ]

    def match(self, url):
        return self.url_regex.search(url) is not None

    def fetch(self, browser, url):
        r = browser.open(url)
        s = BeautifulSoup(r.read())

        panel = s.find("div", {"class" : "def-panel"});

        word = panel.find("div", {"class" :
            "def-header"}).find('a').string.strip();

        definition = panel.find('div', {"class" : 'meaning'}).string.strip()

        title = "Urban Dictionary: " + word

        return { 'title' : title, 'description' : definition }

instantiate = UrbanDictionaryHelper

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
