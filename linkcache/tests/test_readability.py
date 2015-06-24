#!/usr/bin/env python
# -*- coding: utf-8 -*-,
import setup

import unittest

import linkcache
import linkcache.browser
import linkcache.helpers.readability

class ReadabilityTests(unittest.TestCase):
    def setUp(self):
        self.helper = linkcache.helpers.readability.instantiate(None)
        self.browser = linkcache.browser.Browser()

    def test_bad_match(self):
        link = "https://www.readability.com/asdarticles/5kxlx1jw"
        ret = self.helper.match(link)
        self.assertFalse(ret)

    def test_good_match(self):
        link = "https://www.readability.com/articles/5kxlx1jw"
        ret = self.helper.match(link)
        self.assertTrue(ret)

    def test_good_fetch(self):
        link = "https://www.readability.com/articles/ly6pnoqr"
        expected_target = "http://www.theguardian.com/commentisfree/2014/may/20/why-did-lavabit-shut-down-snowden-email"
        expected_title = "Secrets, lies and Snowden's email: why I was forced to shut down Lavabit | Comment is free | The Guardian"
        ret = self.helper.fetch(self.browser, link)

        self.assertTrue('title' in ret)
        self.assertTrue(ret['title'] == expected_title)

        self.assertTrue('url' in ret)
        self.assertTrue(ret['url'] == expected_target)

if __name__ == '__main__':
    unittest.main()

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
