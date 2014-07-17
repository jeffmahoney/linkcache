#!/usr/bin/env python
# -*- coding: utf-8 -*-,

import sql
import os
from pysqlite2 import dbapi2 as sqlite3

class LinkSqlite(sql.LinkSql):
    auto_increment = "AUTOINCREMENT"
    field_placeholder = "?"
    def __init__(self, config):
        sql.LinkSql.__init__(self, config)
        self.filename = config['filename']
        self.db = None
        self.retries = 2
        self.connect()

    def connect(self):
        create = os.path.exists(self.filename) is False
        self.db = sqlite3.connect(self.filename,
                                  detect_types=sqlite3.PARSE_COLNAMES)
        if create:
            self.create_tables()

    def execute(self, command, args):
        cursor = self.db.cursor()
        cursor.execute(command, args)
        self.db.commit()

    def query_one(self, command, args):
        for i in range(0, self.retries):
            try:
                cursor = self.db.cursor()
                cursor.execute(command, args)
            except sqlite3.OperationalError, e:
                print e
                self.db.close()
                self.db = None
                self.connect()

        return cursor.fetchone()

instantiate = LinkSqlite

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
