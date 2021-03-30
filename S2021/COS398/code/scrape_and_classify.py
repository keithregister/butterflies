import json 
import flickrapi
import requests
import matplotlib.pyplot as plt
import numpy as np
import PIL
from PIL import Image
import cv2
import math


def resize(image):
    
    h = image.shape[0]
    w = image.shape[1]
    if h > w:
        newH = 224
        newW = round(w * newH/h)
        resized = cv2.resize(image, (newW, newH))
        padding = abs(224 - newW)
        final = cv2.copyMakeBorder(resized, top = 0, bottom = 0, left = padding//2, right = math.ceil(padding/2), borderType = cv2.BORDER_REFLECT)
    else:
        newW = 224
        newH = round(h*newW/w)
        resized = cv2.resize(image, (newW, newH))
        padding = abs(224 - newH)
        final = cv2.copyMakeBorder(resized, top = padding//2, left = 0, right = 0, bottom = math.ceil(padding/2), borderType = cv2.BORDER_REFLECT)

    return final

api_key = u'e2687aab57bab0c1a5f39a811e15b36c'
api_secret = u'1bee25dbc5f73387'

flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')

model = keras.models.load_model('ResNet152V2-cloud.h5')

classified_as_monarch = 0
monarch_urls = []
for pageNum in range(40):
    photos = flickr.photos.search(text = "butterfly -monarch",
        sort = "relevance",
        per_page='100',
        min_taken_date="2011-01-01 00:00:00",
        max_taken_date="2011-02-01 00:00:00",
        page = pageNum)

    for pic in photos["photos"]["photo"]:
        url = "https://live.staticflickr.com/{}/{}_{}.jpg".format(pic["server"], pic["id"], pic["secret"])
        im = Image.open(requests.get(url, stream=True).raw)
        x = np.asarray(im)
        proper_im = resize(x)
        butterfly_im = proper_im[None, :]
        butterfly_pred = model(butterfly_im, training=False)
        butterfly_pred = np.array(butterfly_pred)
        if butterfly_pred[0, 0] > 0.999:
            classified_as_monarch += 1
            monarch_urls.append(url)

with open('classified_monarch_urls.txt', 'w') as filehandle:
    for monarch_url in monarch_urls:
        filehandle.write('%s\n' % monarch_url)