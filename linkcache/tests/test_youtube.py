#!/usr/bin/env python
import setup
import unittest

from linkcache import browser
from linkcache.helpers import youtube

class YoutubeTestCase(unittest.TestCase):
    def setUp(self):
        self.browser = browser.SingletonBrowser()
        self.helper = youtube.instantiate(None)

    def test_matching(self):
        link = "https://www.youtube.com/eRvk5UQY1Js"
        self.assertTrue(self.helper.match(link))

        link = "https://www.youtube.com/watch?v=eRvk5UQY1Js"
        self.assertTrue(self.helper.match(link))

        link = "https://youtu.be/Ldgp3Ton7R4"
        self.assertTrue(self.helper.match(link))

        link = "https://youtu.be/watch?v=Ldgp3Ton7R4"
        self.assertTrue(self.helper.match(link))

        link = "http://www.youtube.com/eRvk5UQY1Js"
        self.assertTrue(self.helper.match(link))

        link = "http://www.youtube.com/watch?v=eRvk5UQY1Js"
        self.assertTrue(self.helper.match(link))

        link = "http://youtu.be/Ldgp3Ton7R4"
        self.assertTrue(self.helper.match(link))

        link = "http://youtu.be/watch?v=Ldgp3Ton7R4"
        self.assertTrue(self.helper.match(link))

        link = "https://www.google.com/"
        self.assertFalse(self.helper.match(link))

    def test_timecode(self):
        title = "She Takes A Photo: 6.5 Years | Beckie0 - YouTube"
        link = "https://youtu.be/eRvk5UQY1Js?t=1m30s"
        url  = "https://www.youtube.com/watch?v=eRvk5UQY1Js#t=1m30s"
        ret = self.helper.fetch(self.browser, link)

        self.assertTrue(ret is not None)
        self.assertTrue(type(ret) == dict)
        self.assertTrue('title' in ret)
        self.assertTrue(ret['title'] == title + " [timecode]")

        self.assertTrue('url' in ret)
        self.assertTrue(ret['url'] == url)


if __name__ == '__main__':
    unittest.main()

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
