import keras
import cv2
import numpy as np
import matplotlib.pyplot as plt

model = keras.models.load_model('ResNet152V2-cloud.h5')
model.summary()
print("loaded model")
monarch_correct = 0
butterfly_correct = 0

for i in range(1100):
  if i % 10 == 0:
    print("on iteration: ", i)
  monarch_path = "test/monarch/image{}.jpg".format(i)
  monarch_im = cv2.imread(monarch_path)

  
  monarch_im = monarch_im[None, :]
  print(monarch_im.shape)
  monarch_pred = model(monarch_im, training=False)
  print(monarch_pred)
'''
  monarch_im = monarch_im[None, :]
  monarch_pred = model(monarch_im, training=False)
  monarch_pred = np.array(monarch_pred)
  if monarch_pred[0, 0] < monarch_pred[0, 1]:
    monarch_correct += 1

  butterfly_path = "test-images/non-monarch/butterfly-{}.jpg".format(i)
  butterfly_im = cv2.imread(butterfly_path)
  butterfly_im = butterfly_im[None, :]
  butterfly_pred = model(butterfly_im, training=False)
  butterfly_pred = np.array(butterfly_pred)
  if monarch_pred[0, 0] > monarch_pred[0, 1]:
    butterfly_correct += 1
'''
