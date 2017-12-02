"""
Example application showing the use of the Translate method in the Text Translation API.
"""

from auth import AzureAuthClient
import requests
import json


def change(text):
    text = text.replace('Röst',' ').replace('röst',' ')
    text = text.replace('sju','<prosody rate="-30.00%">sju</prosody>')
    text = text.replace('är', '<prosody rate="-40.00%">&#603;r</prosody>')
    text = text.replace('så','så,')
    text = text.replace('roligt', '<prosody contour="(80%,+20%) (90%,+30%)">roligt</prosody>')
    text = text.replace('väldigt', '<prosody contour="(80%,+20%) (90%,+30%)">väldigt</prosody>')
    text = text.replace('ä', '&#228;').replace('Ä', '&#196;')
    text = text.replace('ö', '&#246;').replace('Ö', '&#214;')
    text = text.replace('ekorre', '<prosody rate="-40.00%">ekorren</prosody>')
    text = text.replace('Ekorrar', '<prosody rate="-40.00%">ekorrar</prosody>')
    text = text.replace('ekorrar', '<prosody rate="-40.00%">ekorrar</prosody>')
    text = text.replace('ett', 'ett,')
    text = text.replace('två', 'två,')
    text = text.replace('tre','tre,')
    text = text.replace('fem', 'fem,')
    text = text.replace('sju ', '&#615;&#649;,')
    text = text.replace('å', '&#229;').replace('Å', '&#197;')
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

        translationData = s.post(translateUrl, data=data, headers=headers, stream=True)
        return bytes(translationData.content)


if __name__ == "__main__":

    client_secret = 'e9fc657f5c9247cfac2a9ff582a91716'
    auth_client = AzureAuthClient(client_secret)

    name = "squirrel"

    s = ""
    data = []
    with open("media/" + name + "/text.json") as f:
        j = json.loads(f.read())
    for c in j:
        data.append((c["start"], c["duration"], c["text"]))
        s += c["text"]
    with open("media/" + name + "/text.txt", 'w') as f:
        f.write(s)

    for i in range(len(data)):
        time, dur, text = data[i]
        bearer_token = 'Bearer ' + auth_client.get_access_token().decode('ascii')
        mp3data = TextToSpeech(bearer_token, text)
        with open("media/{}/{}.mp3".format(name, i), 'wb') as f:
            f.write(mp3data)
