#!/usr/bin/env python
# -*- coding: utf-8 -*-,
import mechanize
import socket
import os
import csv
import gzip
import errno

class Browser(mechanize.Browser):
    def __init__(self, cookiejar=None, passwords=None):
        mechanize.Browser.__init__(self)
        cj = None
        self.cjfile = cookiejar
        if cookiejar:
            cj = mechanize.MozillaCookieJar()
            if os.path.exists(cookiejar):
                cj.load(cookiejar)
            self.set_cookiejar(cj)

        self.cj = cj

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
                self.add_password(*row)
            f.close()
        self.set_handle_robots(False)
        self.set_handle_refresh(False)
        self.addheaders = [
            ('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.13+ (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2')
        ]
        self.set_debug_http(False)

    def open(self, url):
        r = mechanize.Browser.open(self, url)
        headers = r.info()
        if 'Content-Encoding' in headers:
            if headers['Content-Encoding'] == 'gzip':
                gz = gzip.GzipFile(fileobj = r, mode = 'rb')
                html = gz.read()
                gz.close()
                headers['Content-type'] = 'text/html; charset=utf-8'
                del headers['Content-Encoding']
                r.set_data(html)
                self.set_response(r)
        if self.cj:
            self.cj.save(self.cjfile)
        return r;

if __name__ == '__main__':
    b = Browser('cookies.txt')

    f = b.open("http://www.ice-nine.org/matt/pics/mjw/2007/10/26")

    print f.read()

# vim: ts=4 sw=4 et
