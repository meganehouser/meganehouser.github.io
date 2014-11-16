#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'meganehouser'
SITENAME = 'ぶりとだいこん'
SITEURL = ''
DISCRIPTION = 'pythonとかclojureとかとか'

PATH = 'content'

TIMEZONE = 'Asia/Tokyo'
DATE_FORMATS = {
    'en': ('usa', '%a, %d %b %Y'),
    'jp': ('jpn', '%Y年%m月%d日(%a)'), }
LOCALE = ['usa', 'jpn', 'en_US', 'ja_JP']

DEFAULT_LANG = 'ja'

SITEURL = 'http://meganehouser.github.io'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),)

# Social widget
SOCIAL = (('twitter', 'http://twitter.com/meganehouser'),
          ('github', 'https://github.com/meganehouser'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

THEME = './theme'

SLUGIFY_SOURCE = 'basename'

YEAR_ARCHIVE_SAVE_AS = 'posts/{date:%Y}/index.html'
MONTH_ARCHIVE_SAVE_AS = 'posts/{date:%Y}/{date:%b}/index.html'
