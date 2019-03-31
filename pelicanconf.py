#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'meganehouser'
SITENAME = 'きんつば'
SITEURL = 'http://meganehouser.github.io'
SITESUBTITLE = 'Pythonとかやるソフトウェアエンジニア'

PATH = 'content'

TIMEZONE = 'Asia/Tokyo'
DATE_FORMATS = {
    'en': ('usa', '%a, %d %b %Y'),
    'jp': ('jpn', '%Y年%m月%d日(%a)'), }
LOCALE = ['usa', 'jpn', 'en_US', 'ja_JP']

DEFAULT_LANG = 'ja'


# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
LINKS = (('ぶりとだいこん', 'http://meganehouser.hatenablog.com/'),)

# Social widget
SOCIAL = (('twitter', 'https://twitter.com/meganehouser'),
          ('github', 'https://github.com/meganehouser'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

THEME = './theme/attila'

SLUGIFY_SOURCE = 'basename'

YEAR_ARCHIVE_SAVE_AS = 'posts/{date:%Y}/index.html'
MONTH_ARCHIVE_SAVE_AS = 'posts/{date:%Y}/{date:%b}/index.html'

HEADER_COVER = '/images/cover.jpg'

# Author
AUTHOR_URL = 'author/{slug}'
AUTHOR_SAVE_AS = 'author/{slug}/index.html'
AUTHORS_SAVE_AS = 'authors.html'

DISPLAY_CATEGORIES_ON_MENU = True
DISPLAY_PAGES_ON_MENU = True

AUTHORS_BIO = {
  "meganehouser": {
    "name": "meganehouser",
    "image": "/images/kaeru.jpg",
    "website": "http://meganehouser.github.io/",
    "github": "meganehouser",
    "twitter": "meganehouser",
    "location": "Tokyo",
    "bio": "Excelおじさんを卒業したPythonおじさん。ハウスとよさこい踊る。隠れF#er。すごいHaskell本読んでく。"
  }
}