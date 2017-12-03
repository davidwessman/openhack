import sys
from pytube import YouTube
from bs4 import BeautifulSoup as bs
import requests
from urllib.parse import urlparse, parse_qs

def get_id(url):
    u_pars = urlparse(url)
    quer_v = parse_qs(u_pars.query).get('v')
    if quer_v:
        return quer_v[0]
    pth = u_pars.path.split('/')
    if pth:
        return pth[-1]

def get_urls(link):
    # playlistLink = 'https://www.youtube.com/playlist?list=PLql1guR0G27vdWY8EM6E8mYWIZhpRrefz'
    playlistLink = link #sys.argv[1]
    r = requests.get(playlistLink)
    page = r.text
    soup = bs(page,'html.parser')
    res = soup.find_all('a', {'class': 'pl-video-title-link'})

    urls = list(map(lambda x: 'https://www.youtube.com' + x.get("href"), res))
    return urls

def dl_video(url):
    print('Downloading   '+url)
    yt = YouTube(url)
    yt.streams.first().download('./media/tmp')

import json
def save_metadata(link):
    urls = get_urls(link)
    descr = []
    titles = []
    for url in urls:
        r = requests.get(url)
        page = r.text
        soup = bs(page,'html.parser')
        title = soup.find(id='eow-title')
        titles.append(title.text.strip().replace('|',''))
        description_tag = soup.find(id='eow-description')
        descr.append(description_tag.text)
    dictionary = dict(zip(titles, descr))
    out_file = open('metadata.json','w')
    json.dump(dictionary, out_file, indent=4)