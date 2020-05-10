import argparse
import time
from os.path import isfile, join
from os import listdir

from distutils.util import strtobool
import numpy as np
import tensorflow as tf
from PIL import Image


def predict(image_path, model):
    """Solve MNIST problem.

    Calculate prediction for passed image based on model.

    Parameters
    ----------
    image_path : str
        Image path for which make prediction.
    model : tf.Keras.model
        Trained model to calculate prediction.
    """
    print("-----------------------------------------------------------")

    # Load image
    image = Image.open(image_path)
    input_data = np.array(image, dtype=np.float)

    # Pretty display in console
    arr = np.where(input_data > 0, 1, 0)
    print(arr)

    start_time = time.time()
    # Get prediction
    result = model.predict_classes(input_data.reshape(1, 28, 28, 1))[0]

    end_time = time.time() - start_time

    print(result)
    print(f"Czas wykonania:\t{round(end_time, 4)}s")
    print("-----------------------------------------------------------\n\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-m',
        '--model_file',
        default='michal_model',
        help='Model to be executed'
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
    model = tf.keras.models.load_model(args.model_file)

    if args.all:
        # Get all filenames in DIRECTORY
        onlyfiles = [f for f in listdir(
            args.directory) if isfile(join(args.directory, f))]
        for filename in sorted(onlyfiles):
            predict(f"{args.directory}{filename}", model)
    else:
        predict(args.image, model)


if __name__ == "__main__":
    main()
