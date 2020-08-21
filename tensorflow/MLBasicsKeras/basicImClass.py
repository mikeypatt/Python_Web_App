from __future__ import absolute_import, division, print_function, unicode_literals

# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras

# Helper libraries
import numpy as np
import matplotlib.pyplot as plt

print(tf.__version__)

fashion_mnist = keras.datasets.fashion_mnist

(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()



class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat', 'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']


#plot initial data
"""
plt.figure()
plt.imshow(train_images[0])
plt.colorbar()
plt.grid(False)
plt.show()
"""

#preproces (normalise to 1)
train_images = train_images / 255.0
test_images = test_images / 255.0

#plot preprocessed data
"""
plt.figure(figsize=(10,10))
for i in range(25):
        plt.subplot(5,5,i+1)
        plt.xticks([])
        plt.yticks([])
        plt.grid(False)
        plt.imshow(train_images[i], cmap=plt.cm.binary)
        plt.xlabel(class_names[train_labels[i]])
plt.show()
"""                            
#Create model
model = keras.Sequential([
        keras.layers.Flatten(input_shape=(28, 28)),
        keras.layers.Dense(128, activation='relu'),
        keras.layers.Dense(10, activation='softmax')
    ])

#Compile model
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy',metrics=['accuracy'])
#fit model
model.fit(train_images, train_labels, epochs=10)

#evaluate accuracy
test_loss, test_acc = model.evaluate(test_images,  test_labels, verbose=2)
print('\nTest accuracy:', test_acc)

#make predicitions
predictions = model.predict(test_images)
print("Argument that the test predicts: ", class_names[np.argmax(predictions[0])])
print("Confidence: ", predictions[0])
print("Actual result: ", class_names[test_labels[0]])
