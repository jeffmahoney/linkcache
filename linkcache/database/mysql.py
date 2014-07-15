#!/usr/bin/env python
import sql
import MySQLdb

class LinkMySql(sql.LinkSql):
    field_placeholder = "%s"
    def __init__(self, config):
        sql.LinkSql.__init__(self, config)

        self.host = config['host']
        self.db = config['name']
        self.user = config['user']
        self.passwd = config['password']
        self.retries = 2

        try:
            self.connect()
        except ImportError, e:
            raise Error("you need python-mysql installed")

    def connect(self):
        self.connection = MySQLdb.connect(db=self.db, user=self.user,
                                passwd=self.passwd, host=self.host,
                                charset='utf8')

    def execute(self, command, args):
        for i in range(0, self.retries):
            try:
                cursor = self.connection.cursor()
                cursor.execute(command, args)
                self.connection.commit()
            except MySQLdb.OperationalError, e:
                self.connect()
            else:
                break

    def query_one(self, command, args):
        for i in range(0, self.retries):
            try:
                cursor = self.connection.cursor()
                cursor.execute(command, args)
            except MySQLdb.OperationalError, e:
                self.connect()
            else:
                break

        if cursor.rowcount == 1:
            return cursor.fetchone()
        elif cursor.rowcount == 0:
            return None

        raise Error("Invalid SQL results: %d results, expected 0 or 1" % cursor.rowcount)

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
