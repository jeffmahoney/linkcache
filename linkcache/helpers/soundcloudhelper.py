#!/usr/bin/env python
# -*- coding: utf-8 -*-,

from common import UrlHelper
import soundcloud
import requests
import re

class SoundCloudHelper(UrlHelper):
    config_section = 'soundcloud'

    def __init__(self, config):
        UrlHelper.__init__(self, config)

        self.provides = [ 'title', 'description' ]
        self.clear_title = True
        self.url_regex = re.compile("soundcloud.com.*")

        self.client = soundcloud.Client(client_id=config['client_id'])

    def fetch(self, browser, url):
        try:
            track = self.client.get('/resolve', url=url)

            trackString = track.title + " by " + track.user['username'] + " on Soundcloud"
            trackDesc = track.description

            return { 'title': trackString,
                     'description': trackDesc }
        except requests.exceptions.HTTPError:
            return { 'title': "SoundCloud - Hear the world’s sounds",
                     'description': "SoundCloud requires JS for all pages, so you don't get any useful data for this non-track link"}

instantiate = SoundCloudHelper
# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
