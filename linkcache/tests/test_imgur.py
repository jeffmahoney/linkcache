#!/usr/bin/env python
# -*- coding: utf-8 -*-,

import setup
import unittest

import linkcache
import linkcache.helpers.imgur
from linkcache import browser
import urllib2

class ImgurTestCase(unittest.TestCase):
    def setUp(self):
        self.helper = linkcache.helpers.imgur.instantiate(None)
        self.browser = browser.SingletonBrowser()

    def test_link_to_image(self):
        ret = self.helper.match("http://imgur.com/askldjaklsd.jpg")
        self.assertTrue(ret)

    def test_link_to_gallery(self):
        ret = self.helper.match("http://imgur.com/gallery/askldjaklsd")
        self.assertFalse(ret)

    def test_missing_link(self):
        link = "http://imgur.com/askldjaklsd.jpg"
        with self.assertRaises(urllib2.HTTPError):
            ret = self.helper.fetch(self.browser, link)

    def test_valid_link(self):
        link = "http://imgur.com/dSC2iva.jpg"
        expected_title = "A monument to lab rats used for DNA research. Novosibirsk, Russia - Imgur"

        ret = self.helper.fetch(self.browser, link)
        self.assertTrue(type(ret) == dict)
        self.assertTrue('title' in ret)
        self.assertTrue(ret['title'] == expected_title)

if __name__ == '__main__':
    unittest.main()

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
