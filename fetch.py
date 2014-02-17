#!/usr/bin/env python

import os
import requests
import praw
from bs4 import BeautifulSoup

def get_reddit_links(subreddit, count):
    pr = praw.Reddit(user_agent='wallpaper-fetcher - Source at github.com/elewis/wallpaper-fetcher')
    return pr.get_subreddit(subreddit).get_hot(limit=count)

def download_image(href, filepath, overwrite=False):
    if not href.startswith('http://'):
        href = 'http://' + href
    if os.path.exists(filepath) and not overwrite:
        print('Skipping download (file already exists)')
        return False
    else:
        stream = requests.get(href, stream=True)
        if stream.status_code == 200:
            with open(filepath, 'wb') as f:
                for block in stream.iter_content():
                    f.write(block)
        return True

def get_imgur_images(href):
    """
    Return list of links to direct images from an imgur page (direct, single image, or album).
    """
    # href is already a direct image link
    if 'i.imgur.com' in href:
        return [str(href)]

    page = BeautifulSoup(requests.get(href).text)
    # Imgur album
    if 'imgur.com/a/' in href:
        return [str(a['href'].lstrip('/')) for a in page.select('.album-view-image-link a')[0]]
    # Single Image
    elif 'imgur.com' in href:
        return [str(page.select('.image a')[0]['href'].lstrip('/'))]
    else:
        raise ValueError('not an imgur link: ' + str(href))



image_accepted = False
print('Fetching top imgur post from /r/wallpapers')
for post in get_reddit_links('wallpapers', 25):
    if 'imgur.com' not in post.url:
        continue

    print('Parsing image location from page...')
    imgur_images = get_imgur_images(post.url)

    print('Downloading image...')
    for url in imgur_images:
        id_, ext = url.split('/')[-1].split('.')
        filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'images', id_ + '.' + ext)
        image_accepted = download_image(url, filepath)

        if image_accepted:
            print('Image saved at "{}"'.format(filepath))
            break
    if image_accepted:
        break

print('Setting as desktop background...')
os.system("gsettings set org.gnome.desktop.background picture-options \"zoom\"")
os.system("gsettings set org.gnome.desktop.background picture-uri \"file://{}\"".format(filepath))
