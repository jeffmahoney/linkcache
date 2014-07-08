#!/usr/bin/env python
import os
import sys
import imp

import sqlite3

def get_module(name):
    if name == 'sqlite3':
        return sqlite3
# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
