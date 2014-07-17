#!/usr/bin/env python
# -*- coding: utf-8 -*-,

from common import UrlHelper
import re
import mechanize

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

        if br.title().find("ogin required") != -1:
            print "Logging into Burrowiki"
            br.open(self.config['loginpage'])
            br.select_form(name="userlogin")
            br.select_form(name="userlogin")
            br['wpName'] = self.config['user']
            br['wpPassword'] = self.config['password']
            br.find_control('wpRemember').items[0].selected = True
            br.submit()
            br.open(url)

        return {
            'description' : br.title(),
            'url' : url
        }

instantiate = BurrowikiHelper
# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
