#!/usr/bin/env python
# -*- coding: utf-8 -*-,
import unittest
import ConfigParser
import json
from urllib import quote_plus

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

    def test_wolframalpha_simple_expression(self):
        expression = "5 + 5"
        ret = self.helper.fetch(self.browser, self.url(expression))
        self.assertTrue(ret['description'] == "5+5: 10")

    def test_interpreted_expression(self):
        expression = "distance to the sun"
        ret = self.helper.fetch(self.browser, self.url(expression))
        self.assertTrue(ret['description'] == 'Sun | distance from Earth: 1.014 au  (astronomical units)')

    def test_wolframalpha_junk(self):
        expression = "slksjdflasknenwnqwn;qlkne;qlkjeocina;sdnfasdf"
        with self.assertRaises(wolframalphahelper.WolframAlphaHelperError):
            ret = self.helper.fetch(self.browser, self.url(expression))

if __name__ == '__main__':
    unittest.main()

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
