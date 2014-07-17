#!/usr/bin/env python
# -*- coding: utf-8 -*-,

import re
import common

selfRefRegex = re.compile(r"http://(www.|)ice-nine.org/(l|link.php)/([A-Za-z0-9]+)")
class IorekShortener(common.GenericShortener):
    def url_to_id(self, id):
        map = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890"
        num = 0
        base = 0
        for chr in id:
            val = map.index(chr)
            if base == 0:
                if val <= 0:
                    raise Exceptiom, "Out of range"
                base = val
            else:
                if val > base:
                    raise Exception, "Out of range(2)"
                val = map.index(chr)
                num *= base
                num += val
        return num

    def map_id(self, id):
        map = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890"
        out = ""
        base = id % 34 + 26
        while id > 0:
            index = id % base
            out = map[index] + out
            id = id / base

        return map[base] + out

    def self_reference(self, url):
        return selfRefRegex.search(url) is not None

    def post_shorten(self, url, id):
        return "http://ice-nine.org/l/%s" % self.map_id(id)

instantiate = IorekShortener

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
