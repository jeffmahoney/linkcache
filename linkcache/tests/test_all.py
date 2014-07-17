#!/usr/bin/env python
# -*- coding: utf-8 -*-,

import setup
import unittest

testmodules = [
	"linkcache.tests.test_browser",
	"linkcache.tests.test_burrowiki",
	"linkcache.tests.test_imgur",
	"linkcache.tests.test_lookup",
	"linkcache.tests.test_readability",
	"linkcache.tests.test_twitter",
	"linkcache.tests.test_youtube",
    ]

suite = unittest.TestSuite()

for t in testmodules:
    try:
        # If the module defines a suite() function, call it to get the suite.
        mod = __import__(t, globals(), locals(), ['suite'])
        suitefn = getattr(mod, 'suite')
        suite.addTest(suitefn())
    except (ImportError, AttributeError):
        # else, just load all the test cases from the module.
        suite.addTest(unittest.defaultTestLoader.loadTestsFromModule(mod))

unittest.TextTestRunner().run(suite)

