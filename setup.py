#!/usr/bin/env python
from setuptools import setup, find_packages
setup(
    name = "linkcache",
    version = "0.9",
    packages = find_packages(),
    package_data = {
        '' : [ "*.dist" "*.txt" ],
        "tests" : [ "passwords.txt" ],
    },

    install_requires = [
        "python_twitter",
        "mechanize",
        "soundcloud",
        "wolframalpha",
    ],

    author = "Jeff Mahoney",
    author_email = "jeffm@jeffreymahoney.com",
    description = "Link caching library",
    license = "GPL v2 only",

    test_suite = "linkcache.tests.test_all",

)

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
