import keras
import tensorflow as tf
from keras.preprocessing.image import ImageDataGenerator

model = tf.keras.applications.ResNet152V2(
    include_top=True,
    weights=None,
    classes=2,
    classifier_activation="softmax",
)
model.compile(optimizer="Adam", loss="binary_crossentropy", metrics=['accuracy'])
model.summary()

trdata = ImageDataGenerator()
traindata = trdata.flow_from_directory(directory="training-images",target_size=(224,224))

hist = model.fit_generator(steps_per_epoch=100, verbose = 1, generator=traindata, validation_split = 0.2, epochs=50)

model.save('ResNet152V2-cloud.h5')
