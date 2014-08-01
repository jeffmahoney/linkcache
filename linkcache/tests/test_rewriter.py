#!/usr/bin/env python
# -*- coding: utf-8 -*-,

import setup
import unittest
import ConfigParser

import linkcache.linkcache

class LookupTestCase(unittest.TestCase):
    def setUp(self):
        config = ConfigParser.ConfigParser()
        f = open('test_rewriter.ini')
        config.readfp(f)
	self.cache = linkcache.linkcache.LinkCache(config)

    def test_google(self):
        ret = self.cache.call_rewriters("@google reference")
        self.assertTrue(ret == "http://www.google.com/search?hl=en&ie=ISO-8859-1&q=reference&btnI=I%27m+Feeling+Lucky")

if __name__ == '__main__':
    unittest.main()

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
