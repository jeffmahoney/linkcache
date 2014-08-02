#!/usr/bin/env python
# -*- coding: utf-8 -*-,

from common import UrlHelper
import wolframalpha
import json
import re

class WolframAlphaHelper(UrlHelper):
    config_section = 'wolframalpha'
    def __init__(self, config):
        UrlHelper.__init__(self, config)
        self.url_regex = re.compile('^(\w*\s*\|\s*|)@calc (.*)')
        self.appid = config['appid']

    def fetch(self, browser, url):
        expression = url
        json_result = {}
        json_result['expression'] = expression
        json_result['result'] = ""
        client = wolframalpha.Client(self.appid)
        res = client.query(url)
        first_result = next(res.results, "")
        if first_result != "":
            json_result['result'] = first_result.text
        return json.dumps(json_result)

instantiate = WolframAlphaHelper
# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
