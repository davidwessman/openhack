# Found in Translation - OpenHack 2017 in Malmö

## Description
This project aims to automate the dubbing of Khan Academy videos into Swedish.
The process to do this involves:

1. Download multiple videos from YouTube at once
2. Transcribe speech into English with timestamps (Voice-to-Text).
3. Translate the text into Swedish.
4. Use Speech Synthesize to generate Swedish voice (Text-to-Voice).
5. Mix together the generated audio clips and synchronize the audio to the video.
6. Upload all the updated videos at once.

## Future improvements
- Better translations as well as Speech synthesize using i.e. Microsoft Cognitive Services.
- More resilient automation.


## Members
- Albin Heimerson
- Cajsa-Lisa Ivarsson
- David Wessman
- Hampus Månefjord
- Josefin Lindström
- Louise Linné
- Miriam Ahlberg
- Ross Linscott

## Dependencies
- Python 3 - for connecting to Microsof Cognitive Services and YouTube.
- PHP - for scraping YouTube for transcripts and translations.
- [FFMPEG](https://www.ffmpeg.org/) - for editing videos using [MoviePy](https://zulko.github.io/moviepy/)
