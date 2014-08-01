#!/usr/bin/env python
# -*- coding: utf-8 -*-,

import sql
import os
#from pysqlite2 import dbapi2 as sqlite3
import sqlite3

class LinkSqlite(sql.LinkSql):
    auto_increment = "AUTOINCREMENT"
    field_placeholder = "?"
    def __init__(self, config):
        sql.LinkSql.__init__(self, config)
        self.filename = config['filename']
        self.db = None
        self.retries = 1
        create = os.path.exists(self.filename) is False

        self.connect()
        if create:
            self.create_tables()
        self.confirm_table()

        self.close()

    def connect(self):
        if self.db is None:
            self.db = sqlite3.connect(self.filename,
                                      detect_types=sqlite3.PARSE_COLNAMES)
    def close(self):
        if self.db:
            self.db.close()
            self.db = None

    def execute(self, command, args):
        self.connect()
        cursor = self.db.cursor()
        cursor.execute(command, args)
        self.db.commit()
        self.close()

    # Leaves the connection open since the fetch will require it
    def query(self, command, args):
        for i in range(0, self.retries + 1):
            try:
                self.connect()
                cursor = self.db.cursor()
                cursor.execute(command, args)
            except sqlite3.OperationalError, e:
                if i < self.retries:
                    print e
                    self.close()
                    self.connect()
                else:
                    raise
            else:
                break

        return cursor

    def query_one(self, query, args):
        cursor = self.query(query, args)
        result = cursor.fetchone()
        self.close()
        return result

    def query_all(self, query, args):
        cursor = self.query(query, args)
        result = cursor.fetchall()
        self.close()
        return result

    def describe(self, table):
        res = self.query_all("PRAGMA TABLE_INFO(%s)" % table, ())
        table = {}
        for row in res:
            table[row[1]] = row[2]

        return table

instantiate = LinkSqlite

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
