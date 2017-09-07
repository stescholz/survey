import numpy as np

from .box import Box


class Question:
    """Models a question in a form.

    Attributes
    ----------
    title : str
        The title of the question.
    answers : list
        The possible answers for each box.
    coords : list
        The list of the coordinates of the center of each box.
    multiple : boolean, optional
        Are multiple answers allowed?

    Parameters
    ----------
    title : str
        The title of the question.
    answers : list
        The possible answers for each box.
    coords : list
        The list of the coordinates of the center of each box.
    multiple : boolean, optional
        Are multiple answers allowed?
    """
    def __init__(self, title, answers, coords, multiple=False):
        self.title = title
        self.answers = answers
        self.coords = coords
        self.multiple = multiple

    def generate_boxes(self, img):
        """"Create the boxes for the question in a form.

        Parameters
        ----------
        img : object
            The Image instance of the form.

        Returns
        -------
        list of Box instance
            The boxes of the question in a form.
        """
        return [Box(left, top, img) for (left, top) in self.coords]

    def get_answers(self, boxes, full=False, tresh=197):
        """Identify the answers to the question.

        Collect the answers of the questions for the boxes. It will  predict
        which box was checked on the form. For decisions it will check for
        errors.

        Parameters
        ----------
        boxes : list
            List of the Box instances for the question.
        full : boolean, optional
            If true, the status of every box of the question is returned.
            Otherwise only the answer is given.
        tresh : int, optional
            The treshold for the mean of the pixels of the box. If the mean is
            below the treshold the box should be checked otherwise not.

        Returns
        -------
        tuple of lists
            The first element is answer or the list of booleans for the answers
            of the question according to the parameter full. And the second
            element is the error message if something is not correct.
        """
        n = len(self.coords)
        answers = [False]*n
        error = ""
        means = np.zeros(n)

        for i, b in enumerate(boxes):
            mean = b.mean()
            means[i] = mean
            if mean < tresh:
                answers[i] = True

        s = sum(answers)
        # yes or no question and no exact answers
        if not self.multiple and s != 1:
            answers = [False]*n

            if s > 1:  # more than one answer - typically a correction was done
                # choose the answer with biggest mean (more white pixels)
                answers[np.argmax(answers)] = True
                error = "(warn) multiple boxes marked - " \
                        "took the one with more white {}".format(means)
            else:
                error = "no boxes marked {}".format(means)

        if not full:
            answers = ", ".join(self.answers[i]
                                for i, ans in enumerate(answers)
                                if ans)

        return answers, error


class YesNoQuestion(Question):
    """Typical yes or no question"""
    def __init__(self, question, coords):
        Question.__init__(self, question, ["ja", "nein"], coords, False)
