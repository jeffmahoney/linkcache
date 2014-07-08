#!/usr/bin/env python

import setup
import unittest

import linkcache.parse

class LookupTestCase(unittest.TestCase):
    def setUp(self):
        self.cache = linkcache.parse.LinkCache()

    def boilerplate(self, line):
        self.cache.parse(url)

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
        self.boilerplate("macos 10.1")


if __name__ == '__main__':
    unittest.main()

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
