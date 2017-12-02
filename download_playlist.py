from pytube import YouTube
from bs4 import BeautifulSoup as bs
import requests

playlistLink = 'https://www.youtube.com/playlist?list=PLql1guR0G27vdWY8EM6E8mYWIZhpRrefz'

r = requests.get(playlistLink)
page = r.text
soup=bs(page,'html.parser')
res=soup.find_all('a',{'class':'pl-video-title-link'})

urls = list(map(lambda x: 'https://www.youtube.com' + x.get("href"), res))

print('STARTING')

for url in urls:
    print('Downloading   '+url)
    yt = YouTube(url)
    yt.streams.first().download('./media/videos')

print('DONE')
