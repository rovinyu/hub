import argparse
import os
import re

FLAGS = None


def process_files(refer_file, input_file):
    if not os.path.exists(refer_file) or not os.path.exists(input_file):
        print("Refer or input file doesn't exist!")
        return

    referf = open(refer_file, 'rt')
    inputf = open(input_file, 'rt')

    outputf = open(FLAGS.output, 'wt')

    rlines = [line.strip() for line in referf]

    for line in inputf:
        found = False
        for rline in rlines:
            tmp = re.split(r'\W+', rline)
            if len(tmp) == 3:
                if tmp[2] == line.strip():
                    outputf.write(line.strip() + " " + tmp[1] + "\n")
                    found = True
                    break
            elif len(tmp) == 2:
                if tmp[1] == line.strip():
                    outputf.write(line.strip() + " " + tmp[0] + "\n")
                    found = True
                    break
            else:
                continue
        if not found:
            outputf.write(line)


    referf.close()
    inputf.close()
    outputf.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--refer',
        type=str,
        default='skeleton_labels.txt',
        help='refer file'
    )
    parser.add_argument(
        '--input',
        type=str,
        default='labels_cn.txt',
        help='input file'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='labels_cn_new.txt',
        help='output file'
    )

    FLAGS, unparsed = parser.parse_known_args()
    process_files(FLAGS.refer, FLAGS.input)