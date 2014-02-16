#! usr/bin/env python

import os
import requests
from bs4 import BeautifulSoup

url = 'http://www.reddit.com/r/wallpapers'

print('Fetching top post from /r/wallpapers...')
page = BeautifulSoup(requests.get(url).text)

entries = page.find_all('p', attrs={'class': 'title'})
links = [str(p.a['href']) for p in entries]

def save_image(href):
    extensions = ('.jpg', '.png', '.jpeg')
    if not href.endswith(extensions):
        href += '.jpg'
    id =  href.split('/')[-1]
    path = 'images/' + id

    stream = requests.get(href, stream=True)
    if stream.status_code == 200:
        with open(path, 'wb') as f:
            for chunk in stream.iter_content():
                f.write(chunk)
    return path

print('Loading "' + links[0] + '"...')
print('Saving image...')
filename = save_image(links[0])
print('Image saved to "' + filename + '"')

print
print('Setting desktop background...')
command = "gsettings set org.gnome.desktop.background picture-uri 'file://{}'"
os.system(command.format(os.path.abspath(filename)))