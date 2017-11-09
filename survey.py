from __future__ import print_function, division

import os
import subprocess
import sys

import matplotlib.pyplot as plt
import numpy as np

from survey import *
from survey.statistic import write_tex
from config import *


def usage():
    """print usage"""
    print("Usage: survey.py <command> [<filename>]")
    print()
    print("commands:")
    print("extract         clear scan folder and extract all scans ")
    print("                from filename to the folder")
    print("evaluate        evaluate the survey and store the results")
    print("evaluate&check  call evaluate and mark box positions in all forms")
    print("analyze         show some hints to adjust the parameters")


def extract(filename):
    """extract images from pdf

    Makes sure the directory exists and is empty.
    Call pdfimages to extract the images from the file to the directory.

    Parameters
    ----------
    filename : str
        The filename of the pdf-file.

    """
    print("check if directory exists")
    if os.path.exists(directory):
        print("clear directory")
        if os.path.isdir(directory):
            for f in os.listdir(directory):
                fn = os.path.join(directory, f)
                if os.path.isfile(fn):
                    os.unlink(fn)
        else:
            print("{} is no directory!".format(directory))
            sys.exit(1)
    else:
        print("create directory")
        os.makedirs(directory)

    print("extract images from pdf")
    cmd = "pdfimages -j {} {}/fragebogen".format(filename, directory)
    subprocess.call(cmd, shell=True)


def evaluate(check=False):
    """Do the evaluation of the survey

    Parameters
    ----------
    check : boolean, optional
        If check is true, then for every the positions of the boxes will be
        marked, see scan directory for the images.
    """
    survey = Survey(directory, questions, header, off_x, off_y, lower, upper)

    print("check positions, see check.png")
    survey.check_positions(original=True)

    print("find answers and store to csv")
    ans = survey.write_answers_to_csv(csv_fn, log="log.html")
    stats = survey.statistics(ans)

    print("store statistics for LaTex report")
    write_tex(stats, "report/data.tex")

    print("store boxes to analyze")
    boxes = survey.get_box_data()
    np.save("boxes", boxes)

    if check:
        print("mark all boxes in the forms, see scan directory")
        survey.check_all()


def show_boxes_around(boxes, mean, bound, max_n=20, r=15):
    """Displays all boxes with a mean around the box with distance r. There
    will be max_n numbers of boxes for each mean value."""

    ind = np.where((mean >= bound-r) & (mean <= bound+r))[0]

    if len(ind) > 0:

        boxes = boxes[ind]
        mean = mean[ind].astype(int)

        # map mean values to indizes
        ind = {}
        for k, v in enumerate(mean):
            ind.setdefault(v, []).append(k)

        max_n = min(max([len(v) for v in ind.values()]), max_n)

        length = Box.length
        n_rows = len(ind.keys())
        data = 255*np.ones((length*n_rows, length*max_n))
        for r, key in enumerate(sorted(ind.keys())):
            for c, v in enumerate(ind[key]):
                if c == max_n:
                    break
                data[r*length:(r+1)*length,
                     c*length:(c+1)*length] = boxes[v].reshape(length, length)

        plt.imshow(data, cmap="gray", interpolation="nearest")
        plt.yticks(range(length//2, n_rows*length, length), sorted(ind))
        plt.xticks([])
        plt.ylabel("Mean")
        plt.title("Boxes around {}".format(bound))
        plt.show()

    else:
        print("nothing near the bound {}".format(bound))


def analyze():
    """Show the histogram of the mean for the boxes and show the boxes around
    lower and upper bound."""
    # read boxes and compute mean
    boxes = np.load("boxes.npy")
    mean = np.mean(boxes, axis=1)

    # sort by mean
    ind = np.argsort(mean)
    boxes = boxes[ind]
    mean = mean[ind]

    n, bins, patches = plt.hist(mean, bins=50)
    m = max(n)
    plt.plot([lower, lower], [0, m], "r-")
    plt.plot([upper, upper], [0, m], "r-")
    plt.xlabel('Mean')
    plt.show()

    show_boxes_around(boxes, mean, lower)
    show_boxes_around(boxes, mean, upper)


if __name__ == "__main__":

    if len(sys.argv) > 1:
        if sys.argv[1] == "extract":
            if len(sys.argv) > 2:
                extract(sys.argv[2])
            else:
                usage()
        elif sys.argv[1] == "evaluate":
            evaluate()
        elif sys.argv[1] == "evaluate&check":
            evaluate(True)
        elif sys.argv[1] == "analyze":
            analyze()
        else:
            usage()
    else:
        usage()
