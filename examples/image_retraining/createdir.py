import argparse
import os
import re

FLAGS = None


def generate_dir(ifile, itree):
    if not os.path.exists(ifile):
        print("Input file doesn't exist: " + ifile)
        return
    if not os.path.exists(itree):
        os.makedirs(itree)

    inputf = open(ifile, 'rt')

    for line in inputf:
        dirname = itree
        for tmp in line.strip().split():
            dirname = os.path.join(dirname, tmp)
        os.makedirs(dirname, exist_ok=True)

    inputf.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--ifile',
        type=str,
        default='skeleton_labels.txt',
        help='input file to create the directory list'
    )
    parser.add_argument(
        '--itree',
        type=str,
        default='output',
        help='directory name'
    )

    FLAGS, unparsed = parser.parse_known_args()
    generate_dir(FLAGS.ifile, FLAGS.itree)