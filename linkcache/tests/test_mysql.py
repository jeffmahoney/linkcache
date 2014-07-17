#!/usr/bin/env python
# -*- coding: utf-8 -*-,

import setup
import unittest

import tempfile
import shutil

import linkcache.database.mysql

url = u"https://github.com/jeffmahoney/linkcache"
flags = 0
content_type = "text/html; charset=utf-8"
channel = ""
private = False

# These should contain non-ascii characters
unicode_title = u"jeffmahoney/linkcache · GitHub"
unicode_user = u"Malmö"
unicode_description = unicode_title

class MySQLTestcase(unittest.TestCase):
    def setUp(self):
        config = { 'host' : '',
                   'name' : '',
                   'user' : '',
                   'password' : '' }
        self.db = linkcache.database.mysql.instantiate(config)

    def tearDown(self):
        self.db.close()

    def test_table_creation(self):
        self.db.confirm_table()

    def test_non_ascii_unicode_user(self):
        self.assertIsInstance(unicode_user, unicode)
        self.db.new_entry(url, None, unicode_user, "title", flags,
                          content_type, "description", channel, private)

    def test_unicode_title(self):
        self.assertIsInstance(unicode_title, unicode)
        self.db.new_entry(url, None, "user", unicode_title, flags,
                          content_type, "description", channel, private)

    def test_unicode_description(self):
        self.assertIsInstance(unicode_description, unicode)
        self.db.new_entry(url, None, "user", "title", flags,
                          content_type, unicode_description, channel, private)

if __name__ == '__main__':
    unittest.main()

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
