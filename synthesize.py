"""
Example application showing the use of the Translate method in the Text Translation API.
"""

from auth import AzureAuthClient
import json
import requests
import time
from functools import reduce


def change(text):
    dict = {}
    dict['Röst'] = ' '
    dict['så'] = 'så,'
    dict['roligt'] = '<prosody contour="(80%,+50%) (90%,+30%)">roligt</prosody>'
    dict['väldigt'] = '<prosody contour="(80%,+50%) (90%,+30%)">väldigt</prosody>'
    dict['ett'] = 'ett,'
    dict['två'] = 'två,'
    dict['tre'] = 'tre,'
    dict['fyra'] = 'fyra,'
    dict['fem'] = 'fem,'
    dict['sex'] = 'sex,'
    dict['sju'] = '<prosody rate="-30.00%">sju</prosody>'
    dict['åtta'] = 'åtta,'
    dict['nio'] = 'nio,'
    dict['ännu'] = 'ännu,'
    dict['är'] = '<prosody rate="-40.00%">&#603;r</prosody>'
    dict['ekorre'] = '<prosody rate="-40.00%">ekorren</prosody>'
    dict['å'] = '&#229;'
    dict['ä'] = '&#228;'
    dict['ö'] = '&#246;'
    for word, initial in dict.items():
        text = text.replace(word.lower(), initial)
    # text = text.replace('Röst', ' ').replace('röst', ' ')
    # text = text.replace('sju', '<prosody rate="-30.00%">sju</prosody>')
    # text = text.replace('är', '<prosody rate="-40.00%">&#603;r</prosody>')
    # text = text.replace('så', 'så,')
    # text = text.replace('roligt', '<prosody contour="(80%,+50%) (90%,+30%)">roligt</prosody>')
    # text = text.replace('väldigt', '<prosody contour="(80%,+50%) (90%,+30%)">väldigt</prosody>')
    # #text = text.replace('ekorre', '<prosody rate="-40.00%">ekorren</prosody>')
    # #text = text.replace('ekorrar', '<prosody rate="-40.00%">ekorrar</prosody>')
    return text


def TextToSpeech(finalToken, text):
    # Call to Microsoft Translator Service
    text = change(text)
    with requests.Session() as s:
        headers = {'Authorization': finalToken,
                   'X-Microsoft-OutputFormat': 'audio-16khz-64kbitrate-mono-mp3',
                   'Content-Type': 'application/ssml+xml'}

        translateUrl = "https://speech.platform.bing.com/synthesize"
        data = '<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" xml:lang="sv-SE"><voice xml:lang="sv-SE" name="Microsoft Server Speech Text to Speech Voice (sv-SE, HedvigRUS)">{}</voice></speak>'.format(text)

        translation = s.post(translateUrl, data=data, headers=headers, stream=True)
        while translation.status_code == 429:
            print("Used all translations this minute, waiting 30 seconds.")
            time.sleep(30)
            translation = s.post(translateUrl, data=data, headers=headers, stream=True)

        if translation.status_code != 200:
            print("[ERROR]: Unable to connect to Microsoft Cognitive Services")
            print("Response code: " + str(translation.status_code))

        return bytes(translation.content)


def synthesize(dir, cap_path):
    client_secret = 'e9fc657f5c9247cfac2a9ff582a91716'
    auth_client = AzureAuthClient(client_secret)

    # name = "squirrel"

    s = ""
    data = []
    with open(dir + cap_path) as f:
        j = json.loads(f.read())
    for c in j:
        data.append((c["start"], c["duration"], c["text"]))
        s += c["text"]
    with open(dir + "text.txt", 'w') as f:
        f.write(s)

    for i in range(len(data)):
        time, dur, text = data[i]
        bearer_token = 'Bearer ' + auth_client.get_access_token().decode('ascii')
        mp3data = TextToSpeech(bearer_token, text)
        with open("media/tmp/{}.mp3".format(i), 'wb') as f:
            f.write(mp3data)
