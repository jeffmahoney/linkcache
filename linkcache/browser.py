#!/usr/bin/env python
# -*- coding: utf-8 -*-,
import requests
import cookielib
import socket
import os
import csv
import gzip
import errno

class Browser:
    def __init__(self, cookiejar=None, passwords=None, capath=True):
        self.passwords = []
        self.cookiejar = cookielib.MozillaCookieJar()
        if cookiejar:
            self.cookiejar.filename = cookiejar
            if os.path.exists(cookiejar):
                self.cookiejar.load()

        socket.setdefaulttimeout(10)

        if passwords:
            try:
                f = open(passwords)
            except IOError, e:
                if e.errno != errno.ENOENT:
                    raise
                f = open(passwords, "w+")
            csvfile = csv.reader(f, delimiter=',', quotechar='"')
            for row in csvfile:
                self.passwords.append((row[0], row[1], row[2]))
            f.close()
        self.addheaders = {
            'User-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.13+ (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
        }

        self.session = requests.Session()
        self.session.cookies = self.cookiejar

        self.capath = capath

    def open(self, url, **kwargs):
        auth = None
        for rule in self.passwords:
            if rule[0][:len(url)] == url:
                auth = (rule[1], rule[2])
        r = self.session.get(url, auth=auth, stream=True,
                             headers=self.addheaders, verify=self.capath,
                             **kwargs)
        r.raise_for_status()
        if self.cookiejar.filename:
            self.cookiejar.save()

        # Requests doesn't natively support a limit on the content size.
        # r.iter_content does and is used internally by Requests to assign
        # to _content, which is used by the other helpers.  This violates
        # the API but to do otherwise means duplicating what Requests does.
        r._content = bytes()
        for chunk in r.iter_content(10*1024*1024):
            r._content += chunk
            if len(r._content) >= 10*1024*1024:
                break
        return r;

    def post(self, url, **kwargs):
        auth = None
        for rule in self.passwords:
            if rule[0][:len(url)] == url:
                auth = (rule[1], rule[2])
        r = self.session.post(url, auth=auth, stream=True,
                              headers=self.addheaders, verify=self.capath,
                              **kwargs)
        r.raise_for_status()
        if self.cookiejar.filename:
            self.cookiejar.save()

        # Requests doesn't natively support a limit on the content size.
        # r.iter_content does and is used internally by Requests to assign
        # to _content, which is used by the other helpers.  This violates
        # the API but to do otherwise means duplicating what Requests does.
        r._content = bytes()
        for chunk in r.iter_content(10*1024*1024):
            r._content += chunk
            if len(r._content) >= 10*1024*1024:
                break
        return r;

if __name__ == '__main__':
    b = Browser('cookies.txt')

    f = b.open("http://www.ice-nine.org/matt/pics/mjw/2007/10/26")
    print type(f)

    print f.text

# vim: ts=4 sw=4 et
