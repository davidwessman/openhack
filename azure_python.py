"""
Example application showing the use of the Translate method in the Text Translation API.
"""

from xml.etree import ElementTree
from auth import AzureAuthClient
import requests
import base64

doItAgain = "yes"

def TextToSpeech(finalToken):
    # Call to Microsoft Translator Service
    with requests.Session() as s:
        headers = {'Authorization': finalToken,
                   'X-Microsoft-OutputFormat': 'audio-16khz-64kbitrate-mono-mp3',
                   'Content-Type': 'application/ssml+xml'}

        translateUrl = "https://speech.platform.bing.com/synthesize"
        data = '<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" xml:lang="sv-SE"><voice xml:lang="sv-SE" name="Microsoft Server Speech Text to Speech Voice (sv-SE, HedvigRUS)">Hej, jag heter Khan och jag har 10 + 5.3 katter, vad blir sin(x)</voice></speak>'

        translationData = s.post(translateUrl, data=data, headers=headers, stream=True)
        file = open('./sound.mp3', 'wb')
        bs = bytes(translationData.content)
        file.write(bs)


if __name__ == "__main__":

    client_secret = 'e9fc657f5c9247cfac2a9ff582a91716'
    auth_client = AzureAuthClient(client_secret)
    bearer_token = 'Bearer ' + auth_client.get_access_token().decode('ascii')
    TextToSpeech(bearer_token)
    print(' ')
