#!/usr/bin/python env
# -*- coding: utf-8 -*-,

class UrlHelper(object):
    config_section = None
    def __init__(self, config):
        if config is None:
            config = {}
        assert type(config) is dict
        self.clear_title = False
        self.url_regex = None
        self.provides = []

    def match(self, url):
        if self.url_regex:
            return self.url_regex.search(url) is not None
        return False;

    def fetch(self, browser, url):
        return {}

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
