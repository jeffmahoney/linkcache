#!/usr/bin/env python
# -*- coding: utf-8 -*-,

import setup
import unittest

import linkcache.linkcache

config = {
    'general' : {
        'database' : 'sqlite3',
        'shortener' : 'none',
        'rewriters' : 'google',
        'helpers' : '',
    },
    'sqlite3' : {
        'filename' : 'test.sqlite3',
    },
    'google' : {
        'regex' : "^(\w*\s*\|\s*|)@google (.*)",
        'rewriter' :
"""
from urllib import urlencode
terms = urlencode({'btnI' : "I'm Feeling Lucky", 'q' : match.group(2)})
line = "http://www.google.com/search?hl=en&ie=ISO-8859-1&%s" % terms
""",
    }
}

class LookupTestCase(unittest.TestCase):
    def setUp(self):
	self.cache = linkcache.linkcache.LinkCache(config)

    def test_google(self):
        ret = self.cache.call_rewriters("@google reference")
        self.assertTrue(ret == "http://www.google.com/search?hl=en&ie=ISO-8859-1&q=reference&btnI=I%27m+Feeling+Lucky")

if __name__ == '__main__':
    unittest.main()

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
