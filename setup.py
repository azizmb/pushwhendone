#!/usr/bin/env python

from distutils.core import setup

setup(
    name='notify-when-done',
    version='1.0',
    description='Send push notifications to monitor long running jobs',
    author='Aziz M. Bookwala',
    author_email='aziz.mansur@gmail.com',
    url='https://github.com/azizmb/pushwhendone',
    py_modules=['notify_when_done'],
    install_requires=[
        'requests',
        'requests[security]',
        'py-notify',
    ],
)
