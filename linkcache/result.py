#!/usr/bin/env python
# -*- coding: utf-8 -*-,

from datetime import datetime
import re

F_SPOILERS = 0x4
F_NSFW = 0x2
F_MAYBE_NSFW = 0x1

M_NSFW = F_NSFW | F_MAYBE_NSFW

class LinkCacheResult:
    def __init__(self, result={}):
        self.url = None
        self.flags = 0
        self.private = False
        self.id = None
        self.count = None
        self.timestamp = None
        self.title = None
        self.first_seen = None
        self.request_timestamp = None
        self.url_line = None
        self.user = None
        self.content_type = None
        self.description = None
        self.shorturl = None
        self.id = None
        self.channel = None

        if type(result) is str:
            self.user = result
            return

        for key, value in result.iteritems():
            setattr(self, key, value)

        if 'timestamp' in result:
            assert(isinstance(result['timestamp'], datetime))

        if 'request_timestamp' in result:
            assert(isinstance(result['request_timestamp'], datetime))

    def timeAgo(self):
        ago = ""
        delta = self.request_timestamp - self.timestamp

        years = int(delta.days / 365.24)
        days = int(delta.days % 365.24)
        weeks = days / 7
        days %= 7

        hours = delta.seconds / (60*60)
        seconds = delta.seconds % (60*60)
        minutes = seconds / 60
        seconds %= 60

        months = 0
        if weeks > 10:
            months = weeks / 4
            days += weeks * 7
            weeks = 0

        if years > 0:
            hours = minutes = seconds = 0
            ago = str(years) + "y"

        if months > 0:
            hours = minutes = seconds = 0
            if ago != "":
                ago += ", "
            ago += str(months) + "m"

        if weeks > 0:
            minutes = seconds = 0
            if ago != "":
                ago += ", "
            ago += str(weeks) + "w"

        if days > 0:
            minutes = seconds = 0
            if ago != "":
                ago += ", "
            ago += str(days) + "d"

        if hours > 0:
            seconds = 0
            if ago != "":
                ago += ", "
            ago += str(hours) + "h"

        if minutes > 0:
            if ago != "":
                ago += ", "
            ago += str(minutes) + "m"

        if seconds > 0:
            if ago != "":
                ago += ", "
            ago += str(seconds) + "s"
        else:
            if ago == "":
                ago = "0s"
            ago += " ago"

        return ago

    def merge_flags(self, new_flags):
        orig = self.flags

        if orig & F_MAYBE_NSFW and new_flags & F_NSFW:
            orig &= ~F_MAYBE_NSFW
        elif orig & F_NSFW and new_flags & F_MAYBE_NSFW:
            new_flags &= ~F_MAYBE_NSFW

        return orig | new_flags

    def pretty_flags(self):
        flags = []
        if self.flags & F_NSFW:
            flags.append("NSFW")
        elif self.flags & F_MAYBE_NSFW:
            flags.append("~NSFW")

        if self.private:
            flags.append("P")

        if self.flags & F_SPOILERS:
            flags.append("SPOILERS")

        if flags:
            return ",".join(flags)
        else:
            return None

    def pretty_title(self):
        title = self.title
        if title:
            title += ""
        else:
            title = self.description.replace("\r\n", "\n")

        flags = self.pretty_flags()
        if flags:
            title = "[" + flags + "] " + title

        return title

    def pretty_stats(self):
        alive = ""
        if not self.alive:
            alive = " DEAD"
        return "[%dx, %s, %s%s] " % (self.count, self.user, self.timeAgo(),
                                     alive)

    def __unicode__(self):
        line = self.pretty_title()
        if line:
            line = '(' + re.sub(r"\n+", "  ", line) + ')'
        else:
            line = ""

        if self.count > 1:
            line += " %s" % self.pretty_stats()

        return line

    def __str__(self):
        return self.__unicode__().encode('utf-8')

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
