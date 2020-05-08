import tensorflow as tf
import argparse
from PIL import Image
import numpy as np
import pprint


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-m',
        '--model_file',
        default='test.tflite',
        help='.tflite model to be executed'
    )
    parser.add_argument(
        '-i',
        '--image',
        default='images/two.bmp',
        help='image to be classified')
    args = parser.parse_args()

    interpreter = tf.lite.Interpreter(model_path=args.model_file)

    interpreter.allocate_tensors()

    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    img = Image.open(args.image).resize((28, 28))
    input_data = np.array(img, dtype=np.float)

    # input_data = np.expand_dims(img, axis=0)
    input_data = np.float32(input_data)

    print(input_details)
    print(output_details)

    print(input_data.astype(int))
    print(input_data.shape)
    input_data.reshape((1, 28, 28, 1))
    print(input_data.shape)

    interpreter.set_tensor(input_details[0]['index'], input_data.reshape(1, 28, 28, 1))
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])

    print(type(input_data))
    print(output_data)
    results = np.squeeze(output_data)
    print(results.argsort()[9])

    top_k = results.argsort()[-5:][::-1]
    pprint.pprint(top_k)