from __future__ import print_function
import wave
# just showing you can import standard python libs

import time
import requests
import operator
import numpy as np

# import http and URl libs
import http.client, urllib.request, urllib.parse, urllib.error, base64, requests, json

# Import library to display results
import matplotlib.pyplot as plt
from flask import Flask
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    subscription_key = '6a294681f0f640f3a8b60b1c7de8ea85'
    uri_base = 'https://eastus.api.cognitive.microsoft.com'
    # Request headers.

    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': subscription_key,
    }
    # Request parameters.

    params = {
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
        'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
    }

    # Enter URL of Images to be sampled by Cognitive Services

    # Example - Taylor Swift Image taken from web search
    body = {'url': 'http://cdn1.theodysseyonline.com/files/2016/01/09/635879625800821251-1566784633_1taylorswift-mug.jpg'}

    # Example - Donald Trump
    # body = {'url': 'http://d.ibtimes.co.uk/en/full/1571929/donald-trump.jpg'}


    try:
       # Execute the REST API call and get the response.
        response = requests.request('POST', uri_base + '/face/v1.0/detect', json=body, data=None, headers=headers,
                                    params=params)

        print('Response:')
        parsed = json.loads(response.text)
        return (json.dumps(parsed, sort_keys=True, indent=2))

    except Exception as e:
        print('Error:')
        print(e)



if __name__ == "__main__":
    app.run()