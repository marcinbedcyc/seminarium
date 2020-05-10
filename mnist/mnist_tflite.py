import argparse
import time
from os.path import isfile, join
from os import listdir

from distutils.util import strtobool
import numpy as np
import tensorflow as tf
from PIL import Image


def predict(image_path, interpreter):
    """Solve MNIST problem.

    Calculate prediction for passed image based on model.

    Parameters
    ----------
    image_path : str
        Image path for which make prediction.
    interpreter : tf.lite.interpreter
        Trained model to calculate prediction loaded as tflite model.
    """
    print("-----------------------------------------------------------")

    # Get output, input details for index
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # Load image
    img = Image.open(f"{image_path}").resize((28, 28))

    # Convert loaded image to np.array
    input_data = np.array(img)
    # Change to float32
    input_data = np.float32(input_data)

    # Convert to 0, 1 to pretty display in console
    arr = np.where(input_data > 0, 1, 0)
    print(arr)

    start_time = time.time()
    # Load data to interpreter
    interpreter.set_tensor(input_details[0]['index'], input_data.reshape(1, 28, 28, 1))
    # Invoke interpreter
    interpreter.invoke()
    # Get output
    output_data = interpreter.get_tensor(output_details[0]['index'])

    end_time = time.time() - start_time

    # Get Result
    results = np.squeeze(output_data)
    print(f"Wynik:\t{results.argsort()[9]}")

    print(f"Czas wykonania:\t{round(end_time, 4)}s")
    print("-----------------------------------------------------------\n\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-m',
        '--model_file',
        default='mnist_model.tflite',
        help='.tflite model to be executed'
    )
    parser.add_argument(
        '-i',
        '--image',
        default='images/2two.bmp',
        help='image to be classified'
    )
    parser.add_argument(
        '-a',
        '--all',
        default="false",
        type=strtobool,
        help='Load all test images from images/'
    )
    parser.add_argument(
        '-d',
        '--directory',
        default="images/",
        help='Path to images'
    )
    args = parser.parse_args()

    # Load model
    interpreter = tf.lite.Interpreter(model_path=args.model_file)
    interpreter.allocate_tensors()

    if args.all:
        # Get all filenames in DIRECTORY
        onlyfiles = [f for f in listdir(args.directory) if isfile(join(args.directory, f))]
        for filename in sorted(onlyfiles):
            predict(f"{args.directory}{filename}", interpreter)
    else:
        predict(args.image, interpreter)


if __name__ == '__main__':
    main()
