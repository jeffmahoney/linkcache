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

    def test_timestamp_type_check(self):
        self.rdict['timestamp'] = None
        with self.assertRaises(AssertionError):
            result = linkcache.result.LinkCacheResult(self.rdict)

    def test_request_timestamp_type_check(self):
        self.rdict['request_timestamp'] = None
        with self.assertRaises(AssertionError):
            result = linkcache.result.LinkCacheResult(self.rdict)

    def test_maybe_nsfw_flag_reporting(self):
        self.rdict['flags'] = linkcache.result.F_MAYBE_NSFW
        result = linkcache.result.LinkCacheResult(self.rdict)
        flags = result.pretty_flags()
        self.assertIsInstance(flags, str)
        self.assertTrue('~NSFW' in flags.split(','))

    def test_nsfw_flag_reporting(self):
        self.rdict['flags'] = linkcache.result.F_NSFW
        result = linkcache.result.LinkCacheResult(self.rdict)
        flags = result.pretty_flags()
        self.assertIsInstance(flags, str)
        self.assertTrue('NSFW' in flags.split(','))

    def test_spoilers_flag_reporting(self):
        self.rdict['flags'] = linkcache.result.F_SPOILERS
        result = linkcache.result.LinkCacheResult(self.rdict)
        flags = result.pretty_flags()
        self.assertIsInstance(flags, str)
        self.assertTrue('SPOILERS' in flags.split(','))

    def test_private_flag_reporting(self):
        self.rdict['private'] = True
        result = linkcache.result.LinkCacheResult(self.rdict)
        flags = result.pretty_flags()
        self.assertIsInstance(flags, str)
        self.assertTrue('P' in flags.split())

    def test_maybe_nsfw_spoilers_flags_reporting(self):
        self.rdict['flags'] = linkcache.result.F_MAYBE_NSFW | \
                              linkcache.result.F_SPOILERS
        result = linkcache.result.LinkCacheResult(self.rdict)
        flags = result.pretty_flags()
        self.assertIsInstance(flags, str)
        self.assertTrue('SPOILERS' in flags.split(','))
        self.assertTrue('~NSFW' in flags.split(','))

    def test_nsfw_spoilers_flags_reporting(self):
        self.rdict['flags'] = linkcache.result.F_NSFW | \
                              linkcache.result.F_SPOILERS
        result = linkcache.result.LinkCacheResult(self.rdict)
        flags = result.pretty_flags()
        self.assertIsInstance(flags, str)
        self.assertTrue('SPOILERS' in flags.split(','))
        self.assertTrue('NSFW' in flags.split(','))

    def test_private_spoilers_flags_reporting(self):
        self.rdict['flags'] = linkcache.result.F_SPOILERS
        self.rdict['private'] = True
        result = linkcache.result.LinkCacheResult(self.rdict)
        flags = result.pretty_flags()
        self.assertIsInstance(flags, str)
        self.assertTrue('SPOILERS' in flags.split(','))
        self.assertTrue('P' in flags.split(','))

    def test_private_maybe_nsfw_flags_reporting(self):
        self.rdict['flags'] = linkcache.result.F_MAYBE_NSFW
        self.rdict['private'] = True
        result = linkcache.result.LinkCacheResult(self.rdict)
        flags = result.pretty_flags()
        self.assertIsInstance(flags, str)
        self.assertTrue('P' in flags.split(','))
        self.assertTrue('~NSFW' in flags.split(','))

    def test_private_nsfw_flags_reporting(self):
        self.rdict['flags'] = linkcache.result.F_NSFW
        self.rdict['private'] = True
        result = linkcache.result.LinkCacheResult(self.rdict)
        flags = result.pretty_flags()
        self.assertIsInstance(flags, str)
        self.assertTrue('P' in flags.split(','))
        self.assertTrue('NSFW' in flags.split(','))

    def test_private_maybe_nsfw_spoilers_flags_reporting(self):
        self.rdict['flags'] = linkcache.result.F_MAYBE_NSFW | \
                              linkcache.result.F_SPOILERS
        self.rdict['private'] = True
        result = linkcache.result.LinkCacheResult(self.rdict)
        flags = result.pretty_flags()
        self.assertIsInstance(flags, str)
        self.assertTrue('P' in flags.split(','))
        self.assertTrue('~NSFW' in flags.split(','))
        self.assertTrue('SPOILERS' in flags.split(','))

    def test_private_nsfw_spoilers_flags_reporting(self):
        self.rdict['flags'] = linkcache.result.F_NSFW | \
                              linkcache.result.F_SPOILERS
        self.rdict['private'] = True
        result = linkcache.result.LinkCacheResult(self.rdict)
        flags = result.pretty_flags()
        self.assertIsInstance(flags, str)
        self.assertTrue('P' in flags.split(','))
        self.assertTrue('NSFW' in flags.split(','))
        self.assertTrue('SPOILERS' in flags.split(','))

    def test_maybe_nsfw_to_nsfw_merging(self):
        self.rdict['flags'] = linkcache.result.F_MAYBE_NSFW
        result = linkcache.result.LinkCacheResult(self.rdict)
        new_flags = result.merge_flags(linkcache.result.F_NSFW)
        self.assertTrue(new_flags == linkcache.result.F_NSFW)

    def test_nsfw_to_maybe_nsfw_merging(self):
        self.rdict['flags'] = linkcache.result.F_NSFW
        result = linkcache.result.LinkCacheResult(self.rdict)
        new_flags = result.merge_flags(linkcache.result.F_MAYBE_NSFW)
        self.assertTrue(new_flags == linkcache.result.F_NSFW)

    def test_spoiler_maybe_nsfw_merging(self):
        self.rdict['flags'] = linkcache.result.F_MAYBE_NSFW
        result = linkcache.result.LinkCacheResult(self.rdict)
        new_flags = result.merge_flags(linkcache.result.F_SPOILERS)
        self.assertTrue(new_flags == linkcache.result.F_MAYBE_NSFW | \
                                     linkcache.result.F_SPOILERS)

    def test_spoiler_nsfw_merging(self):
        self.rdict['flags'] = linkcache.result.F_NSFW
        result = linkcache.result.LinkCacheResult(self.rdict)
        new_flags = result.merge_flags(linkcache.result.F_SPOILERS)
        self.assertTrue(new_flags == linkcache.result.F_NSFW | \
                                     linkcache.result.F_SPOILERS)

if __name__ == '__main__':
    unittest.main()

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
