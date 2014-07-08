#!/usr/bin/env python

from datetime import datetime

class LinkCacheResult:
    def __init__(self, result={}):
        self.url = None
        self.nsfw = 0
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

        if type(result) is str:
            self.user = result
            return

        for key, value in result.iteritems():
            setattr(self, key, value)

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

    def __str__(self, with_description=True):
        desc = ""
        if self.title:
            desc += '(' + self.title.replace("\n", "") + ')'
        elif self.description:
            desc += '(' + self.description.replace("\n", "") + ')'
        if self.count > 1:
            if desc != "":
                desc += " "
            alive = ""
            if not self.alive:
                alive = " DEAD"
            desc += "[%dx, %s, %s%s] " % (self.count, self.user,
                                          self.timeAgo(), alive)
        str = self.shorturl
        if with_description:
            str += "\n" + desc

        return str

    def pretty_title(self):
        print "1----"
        title = self.title
        if title is None:
            title = ""
        else:
            title += ""
        if self.nsfw > 0 or self.private:
            title += " ("

            if self.nsfw & 2:
                title += "NSFW"
            elif self.nsfw & 1:
                title += "~NSFW"
            if self.nsfw & 4:
                if self.nsfw != 4:
                    title += ","
                title += "SPOILERS"

            if self.private:
                if self.nsfw > 0:
                    title += ","
                title += "P"

            title += ")"
        print "2---"
        return title

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
