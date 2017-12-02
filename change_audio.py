import json
import moviepy.editor as mp

name = 'squirrel'
video = mp.VideoFileClip('./media/' + name + '.mp4')

with open("media/" + name + "/text.json") as f:
    j = json.loads(f.read())
    starts = list(map(lambda c: float(c['start']), j))

nbrClips = len(starts)

clips = list(map(lambda s: mp.AudioFileClip("./media/{}/{}.mp3".format(name, s)), range(nbrClips)))
clips = list(map(lambda c: c.subclip(0, c.duration*0.8), clips))

print(starts)

current = 0

make_frame = lambda t: [0]
padded_clips = []
for i in range(nbrClips):
    if current < starts[i]:
        padded_clips.append(mp.AudioClip(make_frame, duration=starts[i] - current))
        current = starts[i]
    padded_clips.append(clips[i])
    current += clips[i].duration

concat = mp.concatenate_audioclips(padded_clips)
concat.write_audiofile('./media/' + name + '_audio.mp3')
video.write_videofile('./media/' + name + '_new.mp4', audio='./media/' + name + '_audio.mp3')
