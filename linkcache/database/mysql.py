#!/usr/bin/env python
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

    def connect(self):
        self.connection = MySQLdb.connect(db=self.db, user=self.user,
                                passwd=self.passwd, host=self.host,
                                charset='utf8')

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

    def query_one(self, command, args):
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

        if cursor.rowcount == 1:
            return cursor.fetchone()
        elif cursor.rowcount == 0:
            return None

        raise IndexError("Invalid SQL results: %d results, expected 0 or 1" % cursor.rowcount)

instantiate = LinkMySql

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
