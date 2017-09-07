import csv
import os
from time import time
import numpy as np

from .form import Form


class Survey:
    """Survey via forms where the answers are given by simple check of boxes

    A survey object analyses a collection of scanned forms. It will perform
    transformations of the images and predict the answers to the questions.

    Attributes
    ----------
    questions : list
        The list of Question instances for the survey.
    forms: list
        The list of Form instance for the survey.

    Parameters
    ----------
    directory : str
        The directory where the images are stored.
    questions : list
        The list of Question instances for the survey.
    header : tupel
        The left, upper, right and lower pixel coordinate of the header of the
        form to adjust all forms.
    offset_x, offset_y : int, optional
        The offset in x and y direction to adjust the position of the boxes.
    """
    def __init__(self, directory, questions, header, offset_x=0, offset_y=0):

        self.questions = questions
        if offset_x != 0 or offset_y != 0:
            self.transform_questions(offset_x, offset_y)

        self.forms = []

        print "start init..."
        start = time()

        print "rotate...",

        for f in sorted(os.listdir(directory)):
            fn = os.path.join(directory, f)
            if os.path.isfile(fn) and f.endswith("jpg"):
                form = Form(fn, questions, header)
                form.rotate()
                self.forms.append(form)
                # break
        print "done"

        # Get left upper corner of the bounding box of the header from the
        # first form. Every form is shifted against this coordinates to get
        # a good match of the boxes
        form = self.forms[0]
        left, upper = form.get_left_upper_bbox_header()

        print "shift...",
        for form in self.forms:
            form.shift(left, upper)
            form.init_questions()
        print "done"

        print "init done ({:.2f}s)".format(time()-start)

    def transform_questions(self, offset_x, offset_y):
        """Transform the coordinates of the boxes of the questions.

        Parameters
        ----------
        offset_x, offset_y : int
            The offset in x and y direction to adjust the position.
        """
        for q in self.questions:
            q.coords = [(x+offset_x, y+offset_y) for x, y in q.coords]

    def get_answers(self):
        """Get all answers of the forms and print errors."""
        result = []

        for i, form in enumerate(self.forms):
            answers, errors = form.get_answers()
            result.append(answers)
            if errors:
                print "Error form {}:".format(i)
                for k, error in errors.items():
                    print "Question <{}>: {}".format(self.questions[k].title,
                                                     error)
        return result

    def get_box_data(self):
        """Get all image data of the boxes."""

        res = [b.data.flatten() for form in self.forms for boxes in form.boxes for b in boxes]

        return np.array(res)

    def write_answers_to_csv(self, fn):
        """Store the answers of the survey to a csv file.

        Parameters
        ----------
        fn : str
            The file name.
        """

        with open(fn, "w") as csvfile:
            cw = csv.writer(csvfile)
            # header
            cw.writerow([q.title for q in self.questions])

            for answers in self.get_answers():
                cw.writerow(answers)
