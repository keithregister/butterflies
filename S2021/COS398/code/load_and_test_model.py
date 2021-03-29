import keras
import cv2
import numpy as np

model = keras.models.load_model('models/ResNet152V2')
model.summary()

monarch_correct = 0
butterfly_correct = 0
for i in range(5000, 7000):
  if i % 10 == 0:
    print("on iteration: ", i)
  monarch_path = "monarch/image{}.jpg".format(i)
  monarch_im = cv2.imread(monarch_path)

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
