import requests
from io import BytesIO
from PIL import Image, ImageDraw
import cognitive_face as CF
from flask import Flask
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    KEY = '6a294681f0f640f3a8b60b1c7de8ea85'  # Replace with a valid subscription key (keeping the quotes in place).
    CF.Key.set(KEY)
    # If you need to, you can change your base API url with:
    # CF.BaseUrl.set('https://westus.api.cognitive.microsoft.com/face/v1.0/detect')

    BASE_URL = 'https://eastus.api.cognitive.microsoft.com/face/v1.0/'  # Replace with your regional Base URL
    CF.BaseUrl.set(BASE_URL)

    # You can use this example JPG or replace the URL below with your own URL to a JPEG image.
    img_url = 'https://raw.githubusercontent.com/malhotraguy/traspod/master/Jeremy2.jpg'
    faces = CF.face.detect(img_url)
    print(faces)
    print(faces[0]['faceRectangle'])


    #Download the image from the url
    response = requests.get(img_url)
    img = Image.open(BytesIO(response.content))

    #For each face returned use the face rectangle and draw a red box.
    draw = ImageDraw.Draw(img)
    for face in faces:
        draw.rectangle(getRectangle(face), outline='red')

    #Display the image in the users default image browser.
    img.show()

    #Convert width height to a point in a rectangle
def getRectangle(faceDictionary):
    rect = faceDictionary['faceRectangle']
    left = rect['left']
    top = rect['top']
    bottom = left + rect['height']
    right = top + rect['width']
    return ((left, top), (bottom, right))

if __name__ == "__main__":
    app.run()