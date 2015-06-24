#!/usr/bin/env python
# -*- coding: utf-8 -*-,
import setup

import unittest

import linkcache
import linkcache.browser
import linkcache.helpers.urbandictionary

class UrbanDictionaryTests(unittest.TestCase):
    def setUp(self):
        self.helper = linkcache.helpers.urbandictionary.instantiate(None)
        self.browser = linkcache.browser.Browser()

    def test_bad_match(self):
        link = "http://www.urbandictionary.com/defien.php?term=Jack+Move"
        ret = self.helper.match(link)
        self.assertFalse(ret)

    def test_good_match(self):
        link = "http://www.urbandictionary.com/define.php?term=Jack+Move"
        ret = self.helper.match(link)
        self.assertTrue(ret)

    def test_good_fetch(self):
        link = "http://www.urbandictionary.com/define.php?term=Jack+Move"

        expected_title = "Urban Dictionary: Jack Move"
        expected_description = "To steal something from someone without their consent. An action which someone does to another person for their personal belongings."

        ret = self.helper.fetch(self.browser, link)

        self.assertTrue('title' in ret)
        self.assertTrue(ret['title'] == expected_title)

        self.assertTrue('description' in ret)
        self.assertTrue(ret['description'] == expected_description)

if __name__ == '__main__':
    unittest.main()

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
