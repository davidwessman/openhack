import moviepy.editor as mp


if __name__ == "__main__":

    # video1 = video1.set_audio(sound2)
    # video2 = video2.set_audio(sound1)
    # video1.write_videofile('video1_sound2.mov', codec='copy')

    clips = list(map(lambda s : mp.AudioFileClip("./media/squirrel/{}.mp3".format(s)), range(20)))

    # make_frame = lambda t : [0]
    # padding = mp.AudioClip(make_frame, duration=3)
    concat = mp.concatenate_audioclips(clips)
    concat.write_audiofile('./media/concat_audio.mp3')
    # concat = mp.CompositeAudioClip(clips);
    # concat.preview()
