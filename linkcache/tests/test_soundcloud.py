#!/usr/bin/env python
# -*- coding: utf-8 -*-,

import setup
import unittest

import linkcache
from linkcache.helpers import soundcloudhelper
from linkcache import browser
import urllib2
import ConfigParser

class SoundCloudTestCase(unittest.TestCase):
    def setUp(self):
        config = ConfigParser.ConfigParser()
        config.read('../config.ini')
        conf = dict(config.items(soundcloudhelper.instantiate.config_section))
        self.helper = soundcloudhelper.instantiate(conf)
        self.browser = browser.SingletonBrowser()

    def test_not_track(self):
        link = "https://soundcloud.com/pages/contact"
        expected_title = "SoundCloud - Hear the world’s sounds"
        expected_desc = "SoundCloud requires JS for all pages, so you don't get any useful data for this non-track link"

        ret = self.helper.fetch(self.browser, link)
        self.assertIsInstance(ret, dict)
        self.assertTrue('title' in ret)
        self.assertTrue(ret['title'] == expected_title)
        self.assertTrue(ret['description'] == expected_desc)

    def test_valid_track(self):
        link = "http://soundcloud.com/evolintent/undertheradar"
        expected_title = "Evol Intent - Under The Radar [FREE DOWNLOAD] by Evol Intent on Soundcloud"
        expected_desc = 'UNDER THE RADAR is a ragga-inspired 170 BPM half-time DNB smasher with hints of skullstep. Definitely a mash of genres, we love it and hope you do too!\r\n\r\n\r\nWeb: http://evolintent.com\r\nLike: https://facebook.com/realevolintent\r\nFollow: http://twitter.com/evol_intent\r\nListen: http://soundcloud.com/evolintent\r\nwatch: http://youtube.com/evolintentrecs'

        ret = self.helper.fetch(self.browser, link)
        self.assertIsInstance(ret, dict)
        self.assertTrue('title' in ret)
        self.assertTrue(ret['title'] == expected_title)
        self.assertTrue(ret['description'] == expected_desc)

    def test_valid_ssl_track(self):
        link = "https://soundcloud.com/ryan-block-10/comcastic-service"
        expected_title = "Comcastic service disconnection by ryan.block on Soundcloud"
        expected_desc = "Please note: this conversation starts about 10 minutes in -- by this point my wife and I are both completely flustered by the oppressiveness of the rep.\r\n\r\nSo! Last week my wife called to disconnect our service with Comcast after we switched to another provider (Astound). We were transferred to cancellations (aka \"customer retention\").\r\n\r\nThe representative (name redacted) continued aggressively repeating his questions, despite the answers given, to the point where my wife became so visibly upset she handed me the phone. Overhearing the conversation, I knew this would not be very fun.\r\n\r\nWhat I did not know is how oppressive this conversation would be. Within just a few minutes the representative had gotten so condescending and unhelpful I felt compelled to record the speakerphone conversation on my other phone.\r\n\r\nThis recording picks up roughly 10 minutes into the call, whereby she and I have already played along and given a myriad of reasons and explanations as to why we are canceling (which is why I simply stopped answering the rep\'s repeated question -- it was clear the only sufficient answer was \"Okay, please don\'t disconnect our service after all.\").\r\n\r\nPlease forgive the echoing and ratcheting sound, I was screwing together some speaker wires in an empty living room!"

        ret = self.helper.fetch(self.browser, link)
        self.assertIsInstance(ret, dict)
        self.assertTrue('title' in ret)
        self.assertTrue(ret['title'] == expected_title)
        self.assertTrue(ret['description'] == expected_desc)

if __name__ == '__main__':
    unittest.main()

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
