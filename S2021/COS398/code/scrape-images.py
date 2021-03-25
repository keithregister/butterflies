limport flickrapi
import json 
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

    final = cv2.cvtColor(final, cv2.COLOR_BGR2RGB)
    return final

api_key = u'e2687aab57bab0c1a5f39a811e15b36c'
api_secret = u'1bee25dbc5f73387'

flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')
photos = flickr.photos.search(text = "butterfly -monarch", sort = "relevance", per_page='100')


for i in range(19, 50):
    print("Iteration: ", i)
    photos = flickr.photos.search(text = "butterfly -monarch", sort = "relevance", per_page='100', page = i)
    for j, pic in enumerate(photos["photos"]["photo"]):
        url = "https://live.staticflickr.com/{}/{}_{}.jpg".format(pic["server"], pic["id"], pic["secret"])
        im = Image.open(requests.get(url, stream=True).raw)
        x = np.asarray(im)
        proper_im = resize(x)
        cv2.imwrite("non-monarchs/image{}.jpg".format(i*100+j), proper_im)



