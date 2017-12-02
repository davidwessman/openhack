import moviepy.editor as mp
video1 = mp.VideoFileClip('./video1.mov')
video2 = mp.VideoFileClip('./video2.mov')
sound1 = mp.AudioFileClip('./video1.mov')
sound2 = mp.AudioFileClip('./video2.mov')

video1 = video1.set_audio(sound2)
video2 = video2.set_audio(sound1)

video1.write_videofile('video1_sound2.mov', codec='copy')
# video1.write_videofile('./video1_sound2.mp4')
# video2.write_videofile('./video2_sound1.mp4')
