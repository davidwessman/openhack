# -*- coding: utf-8 -*-

# PREREQUISITES
# The pip package management tool
# The Google APIs Client Library for Python:
#   pip install --upgrade google-api-python-client
# The google-auth, google-auth-oauthlib, and google-auth-httplib2 for user authorization.
#   pip install --upgrade google-auth google-auth-oauthlib google-auth-httplib2
# The Flask Python web application framework (if you are running the Python samples for web server applications).
#   pip install --upgrade flask
# The requests HTTP library.
#   pip install --upgrade requests
# based on: https://developers.google.com/youtube/v3/docs/videos/insert

import os

#import httplib
import httplib2
import random
import time
import google.oauth2.credentials

import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from apiclient.http import MediaFileUpload

from os import listdir
from os.path import join
from googletrans import Translator

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret.
CLIENT_SECRETS_FILE = "client_secret.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'


def get_authenticated_service():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_console()
    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)
# AIzaSyDiITcL06yKnFiWhXg9iVgQE-xxPLT3UQg # <-- API key 

# Explicitly tell the underlying HTTP transport library not to retry, since
# we are handling retry logic ourselves.
httplib2.RETRIES = 1

# Maximum number of times to retry before giving up.
MAX_RETRIES = 10

# Always retry when these exceptions are raised.
#RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError, httplib.NotConnected,
 #                       httplib.IncompleteRead, httplib.ImproperConnectionState,
  #                      httplib.CannotSendRequest, httplib.CannotSendHeader,
   #                     httplib.ResponseNotReady, httplib.BadStatusLine)

# Always retry when an apiclient.errors.HttpError with one of these status
# codes is raised.
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]


# This method implements an exponential backoff strategy to resume a
# failed upload.
def resumable_upload(request, resource, method):
    response = None
    error = None
    retry = 0
    while response is None:
        try:
            print("Uploading file...")
            status, response = request.next_chunk()
            if response is not None:
                if method == 'insert' and 'id' in response:
                    print(response)
                elif method != 'insert' or 'id' not in response:
                    print(response)
                else:
                    exit("The upload failed with an unexpected response: %s" % response)
        except HttpError as e:
            if e.resp.status in RETRIABLE_STATUS_CODES:
                error = "A retriable HTTP error %d occurred:\n%s" % (e.resp.status,
                                                                     e.content)
            else:
                raise
        #except RETRIABLE_EXCEPTIONS as e:
         #   error = "A retriable error occurred: %s" % e

        if error is not None:
            print(error)
            retry += 1
            if retry > MAX_RETRIES:
                exit("No longer attempting to retry.")

            max_sleep = 2 ** retry
            sleep_seconds = random.random() * max_sleep
            print("Sleeping %f seconds and then retrying..." % sleep_seconds)
            time.sleep(sleep_seconds)


def print_response(response):
    print(response)


# Build a resource based on a list of properties given as key-value pairs.
# Leave properties with empty values out of the inserted resource.
def build_resource(properties):
    resource = {}
    for p in properties:
        # Given a key like "snippet.title", split into "snippet" and "title", where
        # "snippet" will be an object and "title" will be a property in that object.
        prop_array = p.split('.')
        ref = resource
        for pa in range(0, len(prop_array)):
            is_array = False
            key = prop_array[pa]

            # For properties that have array values, convert a name like
            # "snippet.tags[]" to snippet.tags, and set a flag to handle
            # the value as an array.
            if key[-2:] == '[]':
                key = key[0:len(key) - 2:]
                is_array = True

            if pa == (len(prop_array) - 1):
                # Leave properties without values out of inserted resource.
                if properties[p]:
                    if is_array:
                        ref[key] = properties[p].split(',')
                    else:
                        ref[key] = properties[p]
            elif key not in ref:
                # For example, the property is "snippet.title", but the resource does
                # not yet have a "snippet" object. Create the snippet object here.
                # Setting "ref = ref[key]" means that in the next time through the
                # "for pa in range ..." loop, we will be setting a property in the
                # resource's "snippet" object.
                ref[key] = {}
                ref = ref[key]
            else:
                # For example, the property is "snippet.description", and the resource
                # already has a "snippet" object.
                ref = ref[key]
    return resource


# Remove keyword arguments that are not set
def remove_empty_kwargs(**kwargs):
    good_kwargs = {}
    if kwargs is not None:
        for key, value in kwargs.items():
            if value:
                good_kwargs[key] = value
    return good_kwargs


def videos_insert(client, properties, media_file, **kwargs):
    resource = build_resource(properties)  # See full sample for function
    kwargs = remove_empty_kwargs(**kwargs)  # See full sample for function
    request = client.videos().insert(
        body=resource,
        media_body=MediaFileUpload(media_file, chunksize=-1,
                                   resumable=True),
        **kwargs
    )

    # See full sample for function
    return resumable_upload(request, 'video', 'insert')


translator = Translator()

if __name__ == '__main__':
    # When running locally, disable OAuthlib's HTTPs verification. When
    # running in production *do not* leave this option enabled.
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    client = get_authenticated_service()
    path = 'videos/'
    for f in listdir(path):
        print('file name: ', f)
        media_file = join(path, f)#'videos/Counting_with small_numbers.mp4'
        translated_title = translator.translate(f[:-(4+12)], src='en', dest='sv').text
        final_title = join(translated_title, ' Khan Academy')
        print('final title: ', final_title)
        if not os.path.exists(media_file):
            exit('Please specify a valid file location.')

        videos_insert(client,
                    {'snippet.categoryId': '22',
                    'snippet.defaultLanguage': '',
                    'snippet.description': 'Description of uploaded video.',
                    'snippet.tags[]': '',
                    'snippet.title': final_title,
                    'status.embeddable': '',
                    'status.license': '',
                    'status.privacyStatus': 'private',
                    'status.publicStatsViewable': ''},
                    media_file,
                    part='snippet,status')

