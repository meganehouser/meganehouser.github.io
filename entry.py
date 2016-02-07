#! /usr/bin/env python
import os
from datetime import datetime
from argparse import ArgumentParser
from pathlib import Path
import requests
import json


FLICKR_URL = 'https://api.flickr.com/services/rest/'


def input_str(name, default):
    print('{0} [{1}]: '.format(name, default))
    value = input('> ')
    if value:
        return value
    else:
        return default


def make_photos(api_key, album, userid, tag):
    jd = json.JSONDecoder()

    def get_json(text):
        json_txt = r.text.replace('jsonFlickrApi(', '').replace(')', '')
        return jd.decode(json_txt)

    query = {'method': 'flickr.photosets.getPhotos',
             'api_key': api_key,
             'user_id': userid,
             'photoset_id': album,
             'format': 'json',
             'extras': 'tags'}
    r = requests.post(FLICKR_URL, query)
    j = get_json(r.text)
    photos = [p['id'] for p in j['photoset']['photo'] if tag in p['tags']]

    photo_links = []
    link_query = {'method': 'flickr.photos.getSizes',
                  'api_key': api_key, 'format': 'json'}
    for pid in photos:
        link_query['photo_id'] = pid
        r = requests.post(FLICKR_URL, link_query)
        j = get_json(r.text)
        photo_link = j['sizes']['size'][5]
        photo_link['photo_id'] = pid
        photo_links.append(photo_link)
    return photo_links


def make_entry(content_dir, category, tags, date, suffix, content):
    cate_dir = os.path.join(content_dir, category)
    p = Path(cate_dir)
    if not p.exists():
        p.mkdir()

    filename = '{0}_{1}.md'.format(date, suffix)
    filepath = os.path.join(cate_dir, filename)
    with open(filepath, 'w') as f:
        f.write("Title: " + os.linesep)
        f.write("Tags: " + ', '.join(tags) + os.linesep)
        f.write("Summary: " + os.linesep)
        if content:
            f.write(os.linesep + content)

        return filepath

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-c", "--category", help="define category")
    parser.add_argument("-d", "--date", help="define date")
    parser.add_argument("-s", "--suffix", help="add file name suffix")
    parser.add_argument("-e", "--edit", action='store_true',
                        help="edit the blog entry")
    parser.add_argument("-p", "--photo", action='store_true',
                        help="make a photo link entry")
    parser.add_argument("-t", "--tag", help="photo tag")
    args = parser.parse_args()

    category = ""
    tags = []
    date = datetime.now()
    suffix = ""

    if args.category:
        category = args.category
    else:
        category = input_str("category", category)

    if args.date:
        date = datetime.strptime(args.date, '%Y-%m-%d')
    else:
        date = input_str("date", '{0:%Y-%m-%d}'.format(date))

    if args.suffix:
        suffix = args.suffix
    else:
        suffix = input_str("suffix", suffix)

    content = ''
    if args.photo:
        api_key = os.environ['Flickr_APIKEY']
        album = os.environ['Flickr_ALBUM']
        userid = os.environ['Flickr_USER']
        photos = make_photos(api_key, album, userid, args.tag)

        link_fmt = "<a href='https://www.flickr.com/photos/{0}/{1}'" \
                   " title='untitled by meganehouser on Flickr'>" \
                   "<img src='{2}' width=640 height=480 alt='untitled'>" \
                   "</a>{3}{3}"
        for p in photos:
            content += link_fmt.format(userid, p['photo_id'], p['source'], os.linesep)

    content_dir = './content'
    if 'blog_dir' in os.environ:
        content_dir = os.environ['blog_dir']

    filepath = make_entry(content_dir, category, tags, date, suffix, content)

    if not args.edit:
        print('create {0}'.format(filepath))
    else:
        editor = 'vim'
        if 'blog_editor' in os.environ:
            editor = os.environ['blog_editor']

        os.system(editor + ' ' + filepath)
