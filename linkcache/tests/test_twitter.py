#!/usr/bin/env python
# -*- coding: utf-8 -*-,
import setup
import unittest

import linkcache
from linkcache.helpers import twitterhelper
from linkcache import browser
import ConfigParser

class TwitterTestCase(unittest.TestCase):
    def setUp(self):
        config = ConfigParser.ConfigParser()
        config.read('../../config.ini')
        conf = dict(config.items(twitterhelper.instantiate.config_section))
        self.helper = twitterhelper.instantiate(conf)
        self.browser = browser.Browser()

    def test_nonstatus_match(self):
        link = "http://twitter.com/askldjaklsdx"
        ret = self.helper.match(link)
        self.assertFalse(ret)

    def test_invalid_link(self):
        link = "https://twitter.com/nanglish/status/213971298371289371289"
        ret = self.helper.fetch(self.browser, link)
        self.assertTrue(ret == None)

    def test_valid_link(self):
        link = "https://twitter.com/nanglish/status/483763105927659521"
        expected_title = "@nanglish: Ask your doctor if birth control is right for you. Then ask your boss. Then ask some judges. Then ask a guy pooping his pants outside Arby's"

        ret = self.helper.fetch(self.browser, link)
        self.assertIsInstance(ret, dict)
        self.assertTrue('description' in ret)
        self.assertTrue(ret['description'] == expected_title)

if __name__ == '__main__':
    unittest.main()

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
