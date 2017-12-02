"""
Example application showing the use of the Translate method in the Text Translation API.
"""

from auth import AzureAuthClient
import requests
import untangle


def change(text):
    text = text.replace('å', '&#229;').replace('Å', '&#197;')
    text = text.replace('ä', '&#228;').replace('Ä', '&#196;')
    text = text.replace('ö', '&#246;').replace('Ö', '&#214;')
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

    data = []
    obj = untangle.parse('timedtext.xml')
    for c in obj.transcript.children:
        data.append((c["start"], c["dur"], c.cdata))
    print(data)

    for i in range(2, 3):
        time, dur, text = data[i]
        bearer_token = 'Bearer ' + auth_client.get_access_token().decode('ascii')
        mp3data = TextToSpeech(bearer_token, text)
        with open("{}.mp3".format(i), 'wb') as f:
            f.write(mp3data)

