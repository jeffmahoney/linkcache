#!/usr/bin/env python
# -*- coding: utf-8 -*-,

import setup
import unittest
import ConfigParser

import linkcache.linkcache

print linkcache.linkcache

class LookupTestCase(unittest.TestCase):
    def setUp(self):
        config = ConfigParser.ConfigParser()
        config.read('../../config.ini')
        self.cache = linkcache.linkcache.LinkCache(config)

    def boilerplate(self, line, inst=linkcache.result.LinkCacheResult):
        ret = self.cache.parse_line(line, "user")
        if inst is None:
            self.assertIsNone(ret)
        else:
            self.assertIsInstance(ret, inst)
        return ret

    def test_http_url(self):
        self.boilerplate("http://www.google.com")

    def test_https_url(self):
        self.boilerplate("https://www.google.com")

    def test_http_ip_address(self):
        self.boilerplate("http://173.194.46.115")

    def test_https_ip_address(self):
        self.boilerplate("https://173.194.46.115")

    def test_interpolated_url(self):
        self.boilerplate("www.google.com")

    def test_interpolated_nonurl(self):
        self.boilerplate("will.i.am")

    def test_interpolated_ip_address(self):
        self.boilerplate("173.194.46.115")

    def test_interoplated_numbers(self):
        self.boilerplate("macos 10.1", None)

    def test_interpolated_with_real_url(self):
        print self.boilerplate("google.com hosts http://google.com/maps").url


if __name__ == '__main__':
    unittest.main()

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
