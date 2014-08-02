#!/usr/bin/env python
# -*- coding: utf-8 -*-,
import unittest
import ConfigParser
import json
from urllib import urlencode

from linkcache import browser
from linkcache.helpers import wolframalphahelper

class WolframAlphaTests(unittest.TestCase):

    def setUp(self):
        config = ConfigParser.ConfigParser()
        config.read('../../config.ini')
        conf = dict(config.items(wolframalphahelper.instantiate.config_section))
        self.browser = browser.SingletonBrowser()
        self.helper = wolframalphahelper.instantiate(conf)

    def test_wolframalpha_simple_expression(self):
        expression = "5 + 5"
        ret = json.loads(self.helper.fetch(self.browser, expression))
        self.assertTrue(ret['expression'] == "5 + 5" and ret['result'] == "10")

    def test_wolframalpha_complex_expression(self):
        expression = "temperature in Washington, DC on October 3, 2012"
        ret = json.loads(self.helper.fetch(self.browser, expression))
        self.assertTrue(ret['result'] == u"(70 to 81) \xb0F (average: 75 \xb0F)\n(Wednesday, October 3, 2012)")

    def test_wolframalpha_junk(self):
        expression = "slksjdflasknenwnqwn;qlkne;qlkjeocina;sdnfasdf"
        ret = json.loads(self.helper.fetch(self.browser, expression))
        self.assertTrue(ret['result'] == "")

    def test_matching(self):
        expression = "please @calc 5 + 5"
        self.helper.match(expression)


if __name__ == '__main__':
    unittest.main()

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
