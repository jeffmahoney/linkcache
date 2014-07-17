#!/usr/bin/env python
# -*- coding: utf-8 -*-,

import os
import glob
import ConfigParser
import importlib

modules = glob.glob(os.path.dirname(__file__)+"/[a-zA-Z]*.py")
__all__ = [ os.path.basename(f)[:-3] for f in modules]

def load(config):
    all_helpers = []
    all_mods = []

    assert type(config) is dict

    helpers = __all__

    if 'helpers' in config['general']:
	    helpers = config['general']['helpers'].split()

    for mod in helpers:
	x = importlib.import_module("linkcache.helpers.%s" % mod)
	all_mods.append(x)

	try:
	    c = config[x.instantiate.config_section]
	except KeyError:
            c = {}
	except AttributeError:
	    continue

	try:
	    all_helpers.append(x.instantiate(c))
	except AttributeError:
	    pass

    return (all_helpers, all_mods)
