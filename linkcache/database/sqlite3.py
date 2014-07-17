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
        self.retries = 1
        self.connect()

    def connect(self):
        create = os.path.exists(self.filename) is False
        self.db = sqlite3.connect(self.filename,
                                  detect_types=sqlite3.PARSE_COLNAMES)
        if create:
            self.create_tables()

        sql.confirm_tables()

    def execute(self, command, args):
        cursor = self.db.cursor()
        cursor.execute(command, args)
        self.db.commit()

    def query(self, command, args):
        for i in range(0, self.retries + 1):
            try:
                cursor = self.db.cursor()
                cursor.execute(command, args)
            except sqlite3.OperationalError, e:
                if i < self.retries:
                    print e
                    self.db.close()
                    self.db = None
                    self.connect()
                else:
                    raise
            else:
                break

        return cursor

    def query_one(self, query, args):
        cursor = self.query(query, args)
        return cursor.fetchone()

    def query_all(self, query, args):
        cursor = self.query(query, args)
        return cursor.fetchall()

    def describe(self, table):
        res = self.query_all("PRAGMA TABLE_INFO(%s)" % table, ())
        table = {}
        for row in res:
            table[row[1]] = row[2]

        return table

instantiate = LinkSqlite

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
