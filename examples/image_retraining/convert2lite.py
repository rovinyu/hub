import argparse
import os
import tensorflow as tf

FLAGS = None


def convert(saved_model_dir, lite_file):
    if not os.path.exists(saved_model_dir):
        print("Input file doesn't exist: " + saved_model_dir)
        return

    converter = tf.lite.TFLiteConverter.from_saved_model(saved_model_dir)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    tflite_model = converter.convert()
    with open(lite_file, "wb") as f:
        f.write(tflite_model)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--input',
        type=str,
        default='',
        help='tensorflow save model directory'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='converted_model.tflite',
        help='converted tensorflow lite model file name'
    )

    FLAGS, unparsed = parser.parse_known_args()
    convert(FLAGS.input, FLAGS.output)