from subprocess import call
import sys
import os
from download_playlist import *
from synthesize import *
from change_audio import *

# get playlist urls
link = sys.argv[1]
urls = get_urls(link)
print(urls)

for url in urls:
    
    # clear old video files
    dir = "media/tmp/"
    files = os.listdir(dir)
    for file in files:
        os.remove(os.path.join(dir,file))

    vid = get_id(url)
    call(["php", "dl_captions.php", vid])

    dl_video(url)
    # temp dl replacement
    # call(["cp", "media/videos/test.mp4", dir])

    # find video file
    files = os.listdir(dir)
    for file in files:
        if (".mp4" in file):
            vid_file = file
            break
    
    cap_file = vid + ".json"

    synthesize(dir, cap_file)
    change_audio(dir, vid_file, cap_file)

