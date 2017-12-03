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


playlistLink = 'https://www.youtube.com/playlist?list=PLql1guR0G27vdWY8EM6E8mYWIZhpRrefz'

r = requests.get(playlistLink)
page = r.text
soup = bs(page,'html.parser')
res = soup.find_all('a', {'class': 'pl-video-title-link'})

print(x)

urls = list(map(lambda x: 'https://www.youtube.com' + x.get("href"), res))
ids = list(map(lambda x: get_id(x), urls))

# for url in urls:
#     print('Downloading   '+url)
#     yt = YouTube(url)
#     yt.streams.first().download('./media/videos')

print('DONE')
