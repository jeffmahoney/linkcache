#!/usr/bin/env python
# -*- coding: utf-8 -*-,
import unittest
import ConfigParser
import json
from urllib import quote_plus

import sys
sys.path.insert(0, "../..")

from linkcache import browser
from linkcache.helpers import wolframalphahelper

class WolframAlphaTests(unittest.TestCase):

    def setUp(self):
        config = ConfigParser.ConfigParser()
        config.read('../../config.ini')
        conf = dict(config.items(wolframalphahelper.instantiate.config_section))
        self.browser = browser.SingletonBrowser()
        self.helper = wolframalphahelper.instantiate(conf)

    @staticmethod
    def url(expression):
        return "http://www.wolframalpha.com/input/?i=%s" % \
                quote_plus(expression)

    def test_did_you_mean(self):
        expression = "googol plex"
        with self.assertRaises(wolframalphahelper.AmbiguousResultError):
            ret = self.helper.fetch(self.browser, self.url(expression))

#    def test_hits(self):
#        expression = "total hits in MLB in 2011"
#        ret = self.helper.fetch(self.browser, self.url(expression))
#        print ret

    def test_wolframalpha_simple_expression(self):
        expression = "5 + 5"
        ret = self.helper.fetch(self.browser, self.url(expression))
        self.assertTrue(ret['description'] == "5+5: 10")

#   Returns data not available
#    def test_batting_average(self):
#        expression = "batting average of david ortiz in 2013"
#        ret = self.helper.fetch(self.browser, self.url(expression))

    def test_interpreted_expression(self):
        expression = "distance to the sun"
        ret = self.helper.fetch(self.browser, self.url(expression))
        expected = "Earth | distance from Sun: 1.016 au  (astronomical units)"
        self.assertTrue(ret['description'] == expected)

    def test_wolframalpha_junk(self):
        expression = "slksjdflasknenwnqwn;qlkne;qlkjeocina;sdnfasdf"
        with self.assertRaises(wolframalphahelper.NoResultError):
            ret = self.helper.fetch(self.browser, self.url(expression))

if __name__ == '__main__':
    unittest.main()

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
