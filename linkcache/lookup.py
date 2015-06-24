#!/usr/bin/env python
# -*- coding: utf-8 -*-,

import helpers
import browser
from bs4 import BeautifulSoup

class Lookup:
    def __init__(self, config, browser):
        self.config = config
        (self.helpers, self.mods) = helpers.load(config)
        self.browser = browser

    def find_helper(self, url):
        for helper in self.helpers:
            if helper.match(url) is True:
                return helper
        return None

    def get_helper_info(self, url):
        helper = self.find_helper(url)

        if helper:
            info = helper.fetch(self.browser, url)
            if info:
                return { 'helper' : helper,
                         'data' : info }
        return None

    @staticmethod
    def get_html_description(html):
        s = BeautifulSoup(html)
        for tag in s.findAll('meta'):
            found = False
            for attr in tag.attrs:
                if len(attr) < 2:
                    continue
                key = attr[0].lower
                value = attr[1].lower

                if (key == 'property' and value == 'og:description') or \
                   (key == 'name' and value == 'description'):
                    found = True

                if key == 'content' and found:
                    return value
        return None

    def get_description(self, url, response):
        helper = self.find_helper(url)

        if helper:
            if 'description' in helper.provides:
                result = helper.fetch(self.browser, url)
                if result:
                    return result['description']
            return None

        try:
            if 'html' not in response.headers['Content-type']:
                return None
        except KeyError, e:
            return None

        try:
            description = get_html_description(response.text)
        except Exception, e:
            print >>sys.stderr, "General exception %s while getting HTML " \
                                "description" % str(e)
            description = None

        return description

    def get_url(self, url, response):
        helper = self.find_helper(url)

        if helper:
            if 'url' in helper.provides:
                result = helper.fetch(self.browser, url)
                if result:
                    return result['url']
            return url

        return url

    def get_title(self, url, response):
        helper = self.find_helper(url)

        if helper:
            if 'title' in helper.provides:
                result = helper.fetch(self.browser, url)
                if result:
                    return result['title']
            return None

        return None

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
