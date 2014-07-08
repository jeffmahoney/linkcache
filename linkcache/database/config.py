#!/usr/bin/env python

import sqlite
import mysql
import db

config = {}
config = dict(config.items() + db.configtemplate.items())
config = dict(config.items() + sqlite.configtemplate.items())
config = dict(config.items() + mysql.configtemplate.items())
