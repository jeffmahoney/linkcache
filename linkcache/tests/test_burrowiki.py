#!/usr/bin/env python
# -*- coding: utf-8 -*-,
import setup
import unittest
import ConfigParser

from linkcache.helpers import burrowiki
from linkcache import browser

class HelperTests(unittest.TestCase):
    def setUp(self):
        config = ConfigParser.ConfigParser()
        config.read('../../config.ini')
        conf = dict(config.items(burrowiki.instantiate.config_section))
        self.helper = burrowiki.instantiate(conf)
        self.browser = browser.Browser()

    def test_public_page(self):
        url = "https://wiki.dosburros.com/index.php/Public:Halloween_Party"
        ret = self.helper.fetch(self.browser, url)
        self.assertTrue(ret['url'] == url)
        self.assertTrue(ret['description'] == "Public:Halloween Party - BurroWiki")

    def test_private_page(self):
        url = "https://wiki.dosburros.com/index.php/Halloween_Party_Invite_List_2015"
        ret = self.helper.fetch(self.browser, url)
        self.assertTrue(ret['url'] == url)
        self.assertTrue(ret['description'] == "Halloween Party Invite List 2015 - BurroWiki")

if __name__ == '__main__':
    unittest.main()

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
