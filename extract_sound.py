import moviepy.editor as mp
import numpy as np
import untangle


if __name__ == "__main__":

    # video1 = video1.set_audio(sound2)
    # video2 = video2.set_audio(sound1)
    # video1.write_videofile('video1_sound2.mov', codec='copy')

    video = mp.VideoClip('./media/squirrel.mp4')
    clips = list(map(lambda s : mp.AudioFileClip("./media/squirrel/{}.mp3".format(s)), range(20)))


    obj = untangle.parse('timedtext.xml')
    starts = np.fromiter(map(lambda s : float(s["start"]), obj.transcript.children), dtype=np.float)
    durations = np.fromiter(map(lambda c : c.duration, clips), dtype=np.float)
    print(np.sum(durations))
    print(starts)

    print(starts - starts[0])
    starts = starts - starts[0]
    diffs = np.zeros(20)
    for i in range(19):
        diffs[i] = round(starts[i+1] - starts[i] - durations[i], 2)

    print(durations)
    print(diffs)

    # make_frame = lambda t : [0]
    # padding = mp.AudioClip(make_frame, duration=3)
    concat = mp.concatenate_audioclips(clips)
    concat.write_audiofile('./media/concat_audio.mp3')
    # concat = mp.CompositeAudioClip(clips);
    # concat.preview()
