#!/usr/bin/env python
# -*- coding: utf-8 -*-,

from common import UrlHelper
import re
import mechanize
from bs4 import BeautifulSoup

class BurrowikiHelper(UrlHelper):
    config_section = "burrowiki"
    def __init__(self, config):
        UrlHelper.__init__(self, config)
        self.clear_title = True
        self.url_regex = re.compile("wiki.dosburros.com/.*")
        self.provides = [ 'description', 'url' ]
        self.config = config

    def fetch(self, browser, url):
        br = browser
        r = browser.open(url)

        s = BeautifulSoup(r.text)
        if "ogin required" in str(s.title).lower():
            params = {
                'wpRemember' : 1,
                'wpName' : self.config['user'],
                'wpPassword' : self.config['password'],
                'action' : 'submitlogin',
                'type' : 'login',
            }

            # We need to get the login token
            r = br.open(self.config['loginpage'])
            s = BeautifulSoup(r.text)
            for inp in s.find("form").findAll("input"):
                if inp['name'] == "wpLoginToken":
                    params['wpLoginToken'] = inp['value']

            r = br.post(self.config['loginpage'], data=params)
            r = br.open(url)
            s = BeautifulSoup(r.text)

        return {
            'description' : s.title.text,
            'url' : url
        }

instantiate = BurrowikiHelper
# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
