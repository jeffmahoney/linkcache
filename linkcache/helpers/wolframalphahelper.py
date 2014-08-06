#!/usr/bin/env python
# -*- coding: utf-8 -*-,

from common import UrlHelper
import wolframalpha
import json
import re
from urllib import unquote_plus

from xml.etree import ElementTree as etree

class NoResultError(Exception):
    pass

class AmbiguousResultError(Exception):
    pass

class WolframAlphaHelper(UrlHelper):
    config_section = 'wolframalpha'
    def __init__(self, config):
        UrlHelper.__init__(self, config)
        self.url_regex = re.compile('http://www.wolframalpha.com/input/\?i=(.*)')
        self.appid = config['appid']

    def fetch(self, browser, url):
        query = self.url_regex.search(url).group(1)
        expression = unquote_plus(query)
        client = wolframalpha.Client(self.appid)
        res = client.query(expression)

        interpretation = None
        result = next(res.results, "")
        if result != "":
            result = result.text

        for pod in res.pods:
            if pod.title == "Input interpretation":
                interpretation = pod.text
            elif not result and pod.title == "Current result":
                result = pod.text
            elif pod.title == "Input":
                interpretation = pod.text

        try:
            if not interpretation:
                interpretation = res.pods[0].text

            if not result:
                result = res.pods[1].text
        except IndexError:
            pass

        if interpretation and result:
            result = "%s: %s" % (interpretation, result)
        else:
            try:
                dyms = res.tree.findall('didyoumeans')[0].findall('didyoumean')
                options = []
                for dym in dyms:
                    options.append(dym.text)
                if len(options) > 1:
                    prefix = "one of "
                else:
                    prefix = ""
                raise AmbiguousResultError("Did you mean %s[%s]?" % \
                                           (prefix, ", ".join(options)))
            except IndexError:
                pass

        if not result:
            raise NoResultError("No results found.")

        return {
            'description' : result,
            'title' : None,
        }

instantiate = WolframAlphaHelper
# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
