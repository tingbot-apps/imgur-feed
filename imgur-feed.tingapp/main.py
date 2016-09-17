import tingbot
from tingbot import *
import feedparser
from urlparse import urlparse
import os
import urllib

# NOTE: change this variable to an RSS feed on Imgur
imgur_rss_url = 'https://imgur.com/r/starwars/rss'
#####

state = {}

def filename_for_url(url):
    return '/tmp/imgur-' + os.path.basename(urlparse(url).path)

@every(minutes=10)
def refresh_feed():
    image_urls = []
    d = feedparser.parse(imgur_rss_url)
    
    for entry in d['entries']:
        if entry.get('media_content'):
            image_urls.append(entry['media_content'][0]['url'])
        if len(image_urls) >= 10:
            continue

    for image_url in image_urls:
        filename = filename_for_url(image_url)
    
        if not os.path.exists(filename):
            urllib.urlretrieve(image_url, filename)

    state['image_urls'] = image_urls
    state['index'] = 0

@every(seconds=10)
def next_image():
    if 'image_urls' not in state:
        return
    
    image_urls = state['image_urls']
    state['index'] += 1
    
    if state['index'] >= len(image_urls):
        state['index'] = 0
    
    image_url = state['image_urls'][state['index']]
    state['image'] = Image.load(filename_for_url(image_url))

def loop():
    if 'image' not in state:
        screen.fill(color='black')
        screen.text('Loading...')
        return
    
    screen.image(state['image'])

# run the app
tingbot.run(loop)
