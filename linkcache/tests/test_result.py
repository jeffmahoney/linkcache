#!/usr/bin/env python
# -*- coding: utf-8 -*-,
import setup
import unittest

import datetime
import linkcache.result

url = u"https://github.com/jeffmahoney/linkcache"
flags = 0
content_type = "text/html; charset=utf-8"
channel = ""
private = False

# These should contain non-ascii characters
unicode_title = u"jeffmahoney/linkcache · GitHub"
unicode_user = u"Malmö"
unicode_description = unicode_title

class ResultTestCase(unittest.TestCase):
    def setUp(self):
        self.rdict = {
            'url' : url,
            'user' : 'user',
            'count' : 1,
            'timestamp' : datetime.datetime.now(),
            'title' : 'title',
            'request_timestamp' : datetime.datetime.now(),
            'alive' : True,
            'flags' : flags,
            'private' : False,
            'type' : content_type,
            'description' : 'description',
            'shorturl' : 'http://ice-nine.org/l/xxxx',
            'id' : 10,
        }

    # Ensure that the strings we define above will actually test what we want
    def test_sanity_test(self):
        self.assertIsInstance(unicode_title, unicode)
        self.assertRaises(UnicodeEncodeError, str, unicode_title)
        self.assertIsInstance(unicode_description, unicode)
        self.assertRaises(UnicodeEncodeError, str, unicode_description)
        self.assertIsInstance(unicode_user, unicode)
        self.assertRaises(UnicodeEncodeError, str, unicode_user)

    def test_unicode_title(self):
        self.rdict['title'] = unicode_title
        result = linkcache.result.LinkCacheResult(self.rdict)
        x = str(result)

    def test_unicode_description(self):
        self.rdict['description'] = unicode_description
        result = linkcache.result.LinkCacheResult(self.rdict)
        x = str(result)

    def test_unicode_user(self):
        self.rdict['user'] = unicode_user
        result = linkcache.result.LinkCacheResult(self.rdict)
        x = str(result)

if __name__ == '__main__':
    unittest.main()

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
