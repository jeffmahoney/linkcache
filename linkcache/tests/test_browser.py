#!/usr/bin/env python
# -*- coding: utf-8 -*-,
import unittest
import requests

import setup
import linkcache.browser
import json

# These test cases could be considered to be testing httpbin.org, but
# we need to have a target somewhere.

class BrowserTest(unittest.TestCase):
    def setUp(self):
        self.browser = linkcache.browser.Browser('cookies.txt', "passwords.txt")

    def test_invalid_name(self):
        with self.assertRaises(requests.exceptions.ConnectionError):
            ret = self.browser.open("http://httpbin.orgx/")

    def test_invalid_path(self):
        with self.assertRaises(requests.exceptions.HTTPError):
            ret = self.browser.open("http://httpbin.org/xyz")

    def test_open_url(self):
        ret = self.browser.open("http://httpbin.org/get")
        self.assertTrue(isinstance(ret, requests.models.Response))

    def test_auth_url(self):
        ret = self.browser.open("http://httpbin.org/basic-auth/user/passwd")
        self.assertTrue(isinstance(ret, requests.models.Response))

    def test_failed_auth_url(self):
        with self.assertRaises(requests.exceptions.HTTPError):
            ret = self.browser.open("http://httpbin.org/basic-auth/user/passwd2")

    def test_gzip(self):
        ret = self.browser.open("http://httpbin.org/gzip")
        self.assertTrue(isinstance(ret, requests.models.Response))
        headers = ret.headers
        self.assertTrue('Content-Encoding' in headers)
        self.assertTrue(headers['Content-Encoding'] == 'gzip')
        self.assertTrue(ret.encoding == None)
        self.assertTrue(headers['Content-Type'] == 'application/json')

    def test_cookies(self):
        ret = self.browser.open("http://httpbin.org/cookies/set?testcase=working")
        self.assertTrue(isinstance(ret, requests.models.Response))
        ret = self.browser.open("http://httpbin.org/cookies")
        v = ret.json()
        self.assertTrue('cookies' in v)
        self.assertTrue('testcase' in v['cookies'])
        self.assertTrue(v['cookies']['testcase'] == 'working')

if __name__ == '__main__':
    unittest.main()
# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
