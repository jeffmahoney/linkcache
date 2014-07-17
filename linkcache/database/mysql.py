#!/usr/bin/env python
# -*- coding: utf-8 -*-,
import sql
import MySQLdb

class LinkMySql(sql.LinkSql):
    auto_increment = "AUTO_INCREMENT"
    field_placeholder = "%s"
    def __init__(self, config):
        sql.LinkSql.__init__(self, config)

        self.host = config['host']
        self.db = config['name']
        self.user = config['user']
        self.passwd = config['password']
        self.retries = 1

        try:
            self.connect()
        except ImportError, e:
            raise UserWarning("you need python-mysql installed")

        self.confirm_table()

    def connect(self):
        self.connection = MySQLdb.connect(db=self.db, user=self.user,
                                passwd=self.passwd, host=self.host,
                                charset='utf8', use_unicode=True)

    def execute(self, command, args):
        for i in range(0, self.retries + 1):
            try:
                cursor = self.connection.cursor()
                cursor.execute(command, args)
                self.connection.commit()
            except MySQLdb.OperationalError, e:
                if i < self.retries:
                    self.connect()
                else:
                    raise
            else:
                break

    def query(self, command, args):
        for i in range(0, self.retries + 1):
            try:
                cursor = self.connection.cursor()
                cursor.execute(command, args)
            except MySQLdb.OperationalError, e:
                if i < self.retries:
                    self.connect()
                else:
                    raise
            else:
                break
        return cursor

    def query_all(self, query, args):
        cursor = self.query(query, args)
        return cursor.fetchall()

    def query_one(self, query, args):
        cursor = self.query(query, args)
        if cursor.rowcount == 1:
            return cursor.fetchone()
        elif cursor.rowcount == 0:
            return None

        raise IndexError("Invalid SQL results: %d results, expected 0 or 1" % cursor.rowcount)

    def describe(self, table):
        res = self.query_all("DESCRIBE %s" % table, ())
        table = {}
        for row in res:
            table[row[0]] = row[1]

        return table

instantiate = LinkMySql

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
