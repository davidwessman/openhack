import moviepy.editor as mp

def pad_clips(clip1, clip2, padding)


if __name__ == "__main__":
    video1 = mp.VideoFileClip('./media/video1.mov')
    video2 = mp.VideoFileClip('./media/video2.mov')
    sound1 = mp.AudioFileClip('./media/video1.mov')
    sound2 = mp.AudioFileClip('./media/video2.mov')

    # video1 = video1.set_audio(sound2)
    # video2 = video2.set_audio(sound1)

    # video1.write_videofile('video1_sound2.mov', codec='copy')

    make_frame = lambda t : [0]
    padding = mp.AudioClip(make_frame, duration=3)
    clip1 = mp.AudioFileClip('./media/sound.mp3')
    clip2 = mp.AudioFileClip('./media/sound.mp3')
    clips = [clip1, padding, clip2];
    # concat = mp.CompositeAudioClip(clips);
    concat = mp.concatenate_audioclips(clips)
    concat.write_audiofile('concat_audio.mp3')
    # concat.preview()
