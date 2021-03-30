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

    final = cv2.cvtColor(final, cv2.COLOR_BGR2RGB)
    return final

api_key = u'e2687aab57bab0c1a5f39a811e15b36c'
api_secret = u'1bee25dbc5f73387'

flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')

counter = 0
testCount = 0
trainCount = 0
valCount = 0
for year in range(2010, 2021):
    for pageNum in range(10):
        print("Currently on year {} and page {}".format(year, pageNum))
        photos = flickr.photos.search(text = "butterfly -monarch",
        sort = "relevance",
        per_page='100',
        min_taken_date="{}-01-01 00:00:00".format(year),
        max_taken_date="{}-01-01 00:00:00".format(year+1),
        page = pageNum)

        for pic in photos["photos"]["photo"]:
            url = "https://live.staticflickr.com/{}/{}_{}.jpg".format(pic["server"], pic["id"], pic["secret"])
            im = Image.open(requests.get(url, stream=True).raw)
            x = np.asarray(im)
            proper_im = resize(x)
            #Save 1/10 of images for testing
            if counter % 10 == 0:
                cv2.imwrite("test/non-monarch/image{}.jpg".format(testCount), proper_im)
                testCount += 1
            #Save 2/10 images for validation
            elif counter % 10 <= 2:
                cv2.imwrite("val/non-monarch/image{}.jpg".format(valCount), proper_im)
                valCount += 1
            #Save 7/10 images for training
            else:
                cv2.imwrite("train/non-monarch/image{}.jpg".format(trainCount), proper_im)
                trainCount += 1
            
            counter += 1
                
