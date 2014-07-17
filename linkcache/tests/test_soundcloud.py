#!/usr/bin/env python
# -*- coding: utf-8 -*-,

import setup
import unittest

import linkcache
from linkcache.helpers import soundcloudhelper
from linkcache import browser
import urllib2
import ConfigParser

class SoundCloudTestCase(unittest.TestCase):
    def setUp(self):
        config = ConfigParser.ConfigParser()
        config.read('../config.ini')
        conf = dict(config.items(soundcloudhelper.instantiate.config_section))
        self.helper = soundcloudhelper.instantiate(conf)
        self.browser = browser.SingletonBrowser()

    def test_not_track(self):
        link = "https://soundcloud.com/pages/contact"
        expected_title = "SoundCloud requires JS for all pages, so you don't get a title for this non-track link"

        ret = self.helper.fetch(self.browser, link)
        self.assertTrue(type(ret) == dict)
        self.assertTrue('title' in ret)
        self.assertTrue(ret['title'] == expected_title)

    def test_valid_track(self):
        link = "http://soundcloud.com/forss/flickermood"
        expected_title = "Flickermood by Forss on Soundcloud"

        ret = self.helper.fetch(self.browser, link)
        self.assertTrue(type(ret) == dict)
        self.assertTrue('title' in ret)
        self.assertTrue(ret['title'] == expected_title)

    def test_valid_ssl_track(self):
        link = "https://soundcloud.com/ryan-block-10/comcastic-service"
        expected_title = "Comcastic service disconnection by ryan.block on Soundcloud"

        ret = self.helper.fetch(self.browser, link)
        self.assertTrue(type(ret) == dict)
        self.assertTrue('title' in ret)
        self.assertTrue(ret['title'] == expected_title)

if __name__ == '__main__':
    unittest.main()

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
