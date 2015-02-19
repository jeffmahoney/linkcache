#!/usr/bin/env python
# -*- coding: utf-8 -*-,

import HTMLParser
import mechanize
import urllib2
import re
import os
import importlib
import ConfigParser
from datetime import datetime

import database
from result import LinkCacheResult
import lookup
import browser

F_SPOILERS = 0x4
F_NSFW = 0x2
F_MAYBE_NSFW = 0x1

class LinkCacheHTTPError(urllib2.HTTPError):
    pass

class ConfigError(Exception):
    pass

class CodeError(Exception):
    pass

ipAddressRegex = re.compile(r"^((((([0-9]{1,3})\.){3})([0-9]{1,3}))((\/[^\s]+)|))$")
urlRegex = re.compile(r"(^|\s+)(([\|\$\!\~\^]+)|)(((([\w\-]+\.)+)([\w\-]+))(((/[\w\-\.%\(\)~]*)+)+|\s+|[\!\?\.,;]+|$)|https?://[^\]>\s]*)")
selfRefRegex = re.compile(r"http://(www.|)ice-nine.org/(l|link.php)/([A-Za-z0-9]+)")
httpUrlRegex = re.compile(r"(([\|\$\!\~\^]+)|)(https?://[^\]>\s]+)", re.I)

class LinkCache:
    def __init__(self, config):
        if isinstance(config, ConfigParser.ConfigParser):
            d = {}
            for section in config.sections():
                d[section] = dict(config.items(section))
            config = d
        else:
            assert type(config) is dict

        self.check_config(config)

        self.config = config

        self.allow_interpolation = True
        if 'allow_interpolation' in config['general']:
            self.allow_interpolation = config['general']['allow_interpolation']

        self.minimum_length = 0
        if 'minimum_length' in config['general']:
            self.minimum_length = config['general']['minimum_length']

        try:
            cookies = config['browser']['cookiejar']
        except KeyError:
            cookies = None
        try:
            passwords = config['browser']['passwords']
        except KeyError:
            passwords = None

        self.browser = browser.SingletonBrowser(cookies, passwords)
        db = config['general']['database']

        if db == 'sqlite3':
            db = 'sqlite'

        if 'sqlite3' in config:
            config['sqlite'] = config['sqlite3']

        try:
            m = importlib.import_module("linkcache.database.%s" % db)
        except ImportError, e:
            raise ConfigError("No module for %s database found (%s)" %
                              (db, str(e)))

        try:
            db_config = config[db]
        except KeyError, e:
            db_config = {}

        self.database = m.instantiate(db_config)

        shortener = config['general']['shortener']
        try:
            m = importlib.import_module("linkcache.shorteners.%s" % shortener)
        except ImportError, e:
            raise ConfigError("No module for %s shortener found (%s)" %
                              (shortener, str(e)))

        try:
            shortener_config = config[shortener]
        except KeyError, e:
            shortener_config = {}

        self.shortener = m.instantiate(shortener_config)
        self.lookup = lookup.Lookup(config)

        self.line_rewriters = []
        if 'rewriters' in config['general']:
            for name in config['general']['rewriters'].split():
                regex = config[name]['regex']
                rewriter = config[name]['rewriter']
                self.line_rewriters.append((re.compile(regex),
                                           compile(rewriter, '', 'exec')))
    @staticmethod
    def check_config(config):
        if 'general' not in config:
            raise ConfigError("No 'general' section in config")
        elif 'database' not in config['general']:
                raise ConfigError("No 'database' in 'general' section of config")
        elif 'shortener' not in config['general']:
                raise ConfigError("No 'shortener' in 'general' section of config")

    def fetch_by_shorturl(self, shorturl):
        result = self.database.fetch_by_shorturl(shorturl)
        if result:
            return LinkCacheResult(result)
        return None

    def fetch_by_url(self, url, channel=""):
        result = self.database.fetch_by_url(url, channel)
        if result:
            return LinkCacheResult(result)
        return None

    def ping_url(self, result, flags, update_count):
        if update_count:
            result.count += 1
            result.last_seen = datetime.utcnow()
            self.database.increment_count(result.id)

        try:
            r = self.browser.open(result.url)
            if not result.alive:
                result.alive = 1
                try:
                    self.database.set_url_alive(result.id)
                except Exception, e:
                    print e
                    print "Failed to mark link alive"
                    return None

            if result.content_type is None:
                header = self.browser.response().info()
                type = None
                if 'Content-type' in header:
                    type = header['Content-type']
                elif 'Content-Type' in header:
                    type = header['Content-Type']
                self.database.set_content_type(result.id, type)
                result.content_type = type

            new_flags = result.merge_flags(flags)
            if result.flags != new_flags:
                result.flags = new_flags
                self.database.set_flags(result.id, new_flags)

            info = None
            if not result.title or result.title == "" or \
               not result.description or result.description == "":
                info = self.lookup.get_helper_info(result.url)

            if info:
                if not result.title and 'title' in info:
                    result.title = info['title']
                    self.database.set_title(result.id, info['title'])

                if (not result.description or result.description == "") and \
                    'description' in info:
                    result.description = info['description']
                    self.database.set_description(result.id, result.description)
        except urllib2.HTTPError, e:
            result.alive = 0
            try:
                self.database.set_url_dead(result.id)
            except Exception, e2:
                pass
            raise
        except UnicodeDecodeError, e:
            pass

    def call_rewriters(self, line):
        def exec_rewriter(rewriter, match):
            ns = { 'match' : match,
                   'line' : None }
            exec rewriter in ns
            return ns['line']

        for rewriter in self.line_rewriters:
            m = rewriter[0].match(line)
            if m:
                res = exec_rewriter(rewriter[1], m)
                if res:
                    return res;

        return None

    def parse_line(self, line, user, update_count=True, channel=""):
        """
        Typical exceptions: urllib2.HTTPError
        """
        interpolated = False
        title = None
        description = None
        content_type = None

        mapped = self.call_rewriters(line)
        if mapped:
            line = mapped

        match = httpUrlRegex.search(line)
        if match:
            print match.groups()
            url = match.group(3)
            mods = match.group(1)
        else:
            match = urlRegex.search(line)
            if match:
                url = match.group(4)
                mods = match.group(2)
            else:
                return None

        private = False
        flags = 0
        if mods:
            if '$' in mods:
                flags |= F_SPOILERS
            if '!' in mods:
                flags |= F_NSFW
            elif '~' in mods:
                flags |= F_MAYBE_NSFW
            if '^' in mods:
                private = True

        result = {}
        result['flags'] = flags
        result['private'] = private

        # URL without a protocol:// prefix
        if not httpUrlRegex.search(url) and self.allow_interpolation:
            interpolated = True

            if re.search(r"^(([0-9]+)\.)+(|[0-9]+)$", url):
                m = ipAddressRegex.search(url)
                if not m:
                    return None

                ip = m.group(2)
                array = ip.split('.', 4)
                if int(array[0]) == 0:
                    return None

                for num in array:
                    if (int(num) >= 255):
                        return None

            url = "http://" + url

        if len(url) < self.minimum_length:
            return None

        # URL referencing the short link
        shorturl = self.shortener.self_reference(url)
        if shorturl:
            result = self.fetch_by_shorturl(url)
            if result is None:
                raise Exception("*** No match for shorturl %s" % url)
            if not channel or result.channel == channel:
                result.last_seen = datetime.utcnow()
                result.count += 1
                self.database.increment_count(result.id)
                return result
            url = result.url

        try:
            result = self.fetch_by_url(url, channel)
        except AssertionError, e:
            raise
        except Exception, e:
            print "EXCEPTION: %s" % str(e)
            result = None

        if result is not None:
            self.ping_url(result, flags, update_count)
            return result

        charset = None
        deferred_exception = None
        try:
            r = self.browser.open(url)
            title = self.browser.title()
            if title is not None:
                title = " ".join(title.split())
                title = unicode(title, self.browser.encoding())

            header = r.info()
            try:
                charset = header.getparam('charset')
            except:
                pass
            if 'Content-type' in header:
                content_type = header['Content-type']
            elif 'Content-Type' in header:
                content_type = header['Content-Type']
        except urllib2.HTTPError, e:
            if interpolated:
                return None
            if mapped is None:
                raise
            deferred_exception = e
        except urllib2.URLError, e:
            if interpolated:
                return None
            if mapped is None:
                raise
            deferred_exception = e
        except mechanize.BrowserStateError, e:
            title = ""
        except HTMLParser.HTMLParseError, e:
            title = ""

        if charset is None:
            charset = 'utf-8'

        info = self.lookup.get_helper_info(url)
        if info:
            helper = info['helper']
            info = info['data']
            if 'url' in info:
                url = info['url']

                try:
                    result = self.fetch_by_url(url, channel)
                except Exception, e:
                    result = None

                if result:
                    self.ping_url(result, flags, update_count)
                    return result

            if 'title' in info:
                title = info['title']

            if 'description' in info:
                description = info['description']
                if helper.clear_title:
                    title = None
        elif deferred_exception:
            raise deferred_exception

        if content_type and 'html' in content_type and not description:
            description = self.lookup.get_html_description(r.read())

        if description:
            if not isinstance(description, unicode):
                description = unicode(description, charset)
            description = description.strip()

        if title is None:
            title = u""
        else:
            if not isinstance(title, unicode):
                title = unicode(title, charset)
            title = title.strip()

        shorturl = self.shortener.pre_shorten(url)

        self.database.new_entry(url, shorturl, user, title, flags,
                                content_type, description, channel, private)

        result = self.fetch_by_url(url, channel)
        if result is None:
            raise RuntimeWarning("Failed to fetch new entry after adding")

        shorturl = self.shortener.post_shorten(url, result.id)
        if shorturl:
            result.shorturl = shorturl
            self.database.update_shorturl(result.id, shorturl)

        return result

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
