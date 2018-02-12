#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name = "heappercent",
    version = "0.1.1",
    packages = find_packages('src'),
    package_dir = { '': 'src'},
    author = "Naftuli Kay",
    author_email = "me@naftuli.wtf",
    url = "https://github.com/naftulikay/heappercent",
    install_requires = [
        'setuptools',
        'six',
        'pint',
        'psutil',
    ],
    include_package_data = True,
    package_data = { '': [
        'fixtures/*.txt'
    ]},
    dependency_links = [],
    entry_points = {
        'console_scripts': [
            'heap-percent = heappercent:main'
        ]
    }
)
