import requests
from io import BytesIO
from PIL import Image, ImageDraw
import cognitive_face as CF
import urllib
import urllib.request as ur
import cv2
import numpy as np
import matplotlib.pyplot as plt

KEY = '6a294681f0f640f3a8b60b1c7de8ea85'  # Replace with a valid subscription key (keeping the quotes in place).
CF.Key.set(KEY)
# If you need to, you can change your base API url with:
# CF.BaseUrl.set('https://westus.api.cognitive.microsoft.com/face/v1.0/detect')

BASE_URL = 'https://eastus.api.cognitive.microsoft.com/face/v1.0/'  # Replace with your regional Base URL
CF.BaseUrl.set(BASE_URL)

# You can use this example JPG or replace the URL below with your own URL to a JPEG image.
img_url = 'https://raw.githubusercontent.com/malhotraguy/traspod/master/1.jpg'
result = CF.face.detect(img_url)
print(result)
#Convert width height to a point in a rectangle
def getRectangle(faceDictionary):
    rect = faceDictionary['faceRectangle']
    left = rect['left']
    top = rect['top']
    bottom = left + rect['height']
    right = top + rect['width']
    return ((left, top), (bottom, right))

#Download the image from the url
response = requests.get(img_url)
img = Image.open(BytesIO(response.content))

#For each face returned use the face rectangle and draw a red box.
draw = ImageDraw.Draw(img)
for face in result:
    draw.rectangle(getRectangle(face), outline='red')

#Display the image in the users default image browser.
img.show()


def url_to_image(url):
    """
    a helper function that downloads the image, converts it to a NumPy array,
    and then reads it into OpenCV format
    """
    resp = ur.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    # return the image
    return image


img = url_to_image(img_url)

plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.axis('off')

height = result[0]['faceRectangle']['height']
left = result[0]['faceRectangle']['left']
top = result[0]['faceRectangle']['top']
width = result[0]['faceRectangle']['width']

plt.imshow(cv2.cvtColor(img[top:top+height, left:left+width], cv2.COLOR_BGR2RGB))
plt.axis('off')

url1 = 'https://raw.githubusercontent.com/malhotraguy/traspod/master/10.jpg'
url2 = 'https://raw.githubusercontent.com/malhotraguy/traspod/master/5.jpg'
url3 = 'https://raw.githubusercontent.com/malhotraguy/traspod/master/4.jpg'
url4 = 'https://raw.githubusercontent.com/malhotraguy/traspod/master/3.jpg'

urls = [url1, url2, url3, url4]
for url in urls:
  plt.imshow(cv2.cvtColor(url_to_image(url), cv2.COLOR_BGR2RGB))
  plt.axis('off')
  plt.show()

  results = []
  for url in urls:
      r = CF.face.detect(url)
      results += r,
all_faceid = [f['faceId'] for image in results for f in image]

test_url = 'https://raw.githubusercontent.com/malhotraguy/traspod/master/2.jpg'
plt.imshow(cv2.cvtColor(url_to_image(test_url), cv2.COLOR_BGR2RGB))
test_result = CF.face.detect(test_url)
test_faceId = test_result[0]['faceId']
for f in all_faceid:
  r = CF.face.verify(f, test_faceId)
  print(r)
identical_face_id = [f for f in all_faceid
                     if CF.face.verify(f, test_faceId)['isIdentical'] == True]
for i in xrange(len(results)):
  for face in results[i]:
    if face['faceId'] in identical_face_id:
      height = face['faceRectangle']['height']
      left = face['faceRectangle']['left']
      top = face['faceRectangle']['top']
      width = face['faceRectangle']['width']
      plt.imshow(cv2.cvtColor(url_to_image(urls[i])[top:top+height, left:left+width], cv2.COLOR_BGR2RGB))
      plt.axis('off')
      plt.show()
