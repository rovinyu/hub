# Copyright 2015 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
# pylint: enable=line-too-long

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import os.path
import re
import glob

import tensorflow as tf

FLAGS = None

MAX_NUM_IMAGES_PER_CLASS = 2 ** 27 - 1  # ~134M

def create_label_file(image_dir):
  """Builds a  label file from the input image directory
  Args:
    image_dir: String path to a folder containing subfolders of images.

  Returns:
  """
  if not tf.gfile.Exists(image_dir):
    tf.logging.error("Image directory '" + image_dir + "' not found.")
    return

  output_dir = os.path.dirname(FLAGS.output_labels)
  ensure_dir_exists(output_dir)

  sub_dirs = sorted(x[0] for x in tf.gfile.Walk(image_dir))
  # The root directory comes first, so skip it.
  is_root_dir = True
  for sub_dir in sub_dirs:
    if is_root_dir:
      is_root_dir = False
      continue
    extensions = sorted(set(os.path.normcase(ext)  # Smash case on Windows.
                            for ext in ['JPEG', 'JPG', 'jpeg', 'jpg', 'png']))
    file_list = []
    # dir_name = os.path.basename(
        # tf.gfile.Walk() returns sub-directory with trailing '/' when it is in
        # Google Cloud Storage, which confuses os.path.basename().
    #    sub_dir[:-1] if sub_dir.endswith('/') else sub_dir)

    dir_name = os.path.relpath(sub_dir, image_dir)

    if dir_name == image_dir:
      continue
    '''
    tf.logging.info("Looking for images in '" + dir_name + "'")
    for extension in extensions:
      file_glob = os.path.join(image_dir, dir_name, '*.' + extension)
      #file_list.extend(tf.gfile.Glob(file_glob))
      file_list.extend(glob.glob(file_glob))
    if not file_list:
      tf.logging.warning('No files found')
      continue
    if len(file_list) < 20:
      tf.logging.warning(
          'WARNING: Folder has less than 20 images, which may cause issues.')
    elif len(file_list) > MAX_NUM_IMAGES_PER_CLASS:
      tf.logging.warning(
          'WARNING: Folder {} has more than {} images. Some images will '
          'never be selected.'.format(dir_name, MAX_NUM_IMAGES_PER_CLASS))
    '''
    label_name = re.sub(r'[^\w]+', ' ', dir_name.lower())
    with tf.gfile.GFile(FLAGS.output_labels, 'a') as f:
      f.write(label_name + '\n')

  return

def ensure_dir_exists(dir_name):
  """Makes sure the folder exists on disk.

  Args:
    dir_name: Path string to the folder we want to create.
  """
  if not os.path.exists(dir_name):
    os.makedirs(dir_name)

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument(
      '--image_dir',
      type=str,
      default='',
      help='Path to folders of labeled images.'
  )
  parser.add_argument(
      '--output_labels',
      type=str,
      default='/tmp/labels.txt',
      help='Where to save labels file.'
  )

  FLAGS, unparsed = parser.parse_known_args()
  tf.logging.set_verbosity(tf.logging.DEBUG)
  create_label_file(FLAGS.image_dir)
