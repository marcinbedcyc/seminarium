import tensorflow as tf
import sys
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import time

if __name__ == "__main__":

    # Restoring model
    start_time = time.time()
    model = tf.keras.models.load_model("model")
    # model.summary()

    # Loading data
    # _, (x_test, y_test) = tf.keras.datasets.mnist.load_data()
    
    # # Data normalization from [0,255] to [0.0,1.0] and proper dimensions
    # x_test_normalized = (x_test/255.0).reshape(x_test.shape[0], 28, 28, 1)

    # model.evaluate(x=x_test_normalized, y=y_test, batch_size=40000)

    # image_index = 7777 # You may select anything up to 60,000
    # print(y_test[image_index]) # The label is 8
    # plt.imshow(x_test[image_index], cmap='Greys')
    # print(x_test[image_index])

    image = Image.open("images/four.bmp")
    data = np.array(image, dtype=np.float)
    data = model.predict_classes(data.reshape(1, 28, 28, 1))[0]
    end_time = time.time() - start_time
    print(data)
    print(f"{end_time:.2}s")