import numpy as np
from PIL import Image


class Form:
    """Represents one form of a survey.

    Attributes
    ----------
    fn : str
        The filename of the image.
    questions : list
        The list of Question instances.
    header : tupel
        The left, upper, right and lower pixel coordinate of the header.
    img : object
        The Image instance of the form.
    boxes : list
        The list of Box instances.

    Parameters
    ----------
    fn : str
        The filename of the image.
    questions : list
        The list of Question instances.
    header : tupel
        The left, upper, right and lower pixel coordinate of the header.

    """
    def __init__(self, fn, questions, header):
        self.fn = fn
        self.questions = questions
        self.header = header

        self.img = Image.open(fn).convert("L")
        self.boxes = []

    def rotate(self, tresh=60):
        """Rotate the form to correct the skew after scanning

        Parameters
        ----------
        tresh : int, optional
            All pixels lower than the treshold are supposed to be black.
        """
        # extract header and do a pca to find the rotation angle
        data = self.get_header_data()

        x, y = np.where(data < tresh)
        eigval, eigvec = np.linalg.eigh(np.cov(np.array([x, y])))
        angle = np.arctan2(eigvec[0, :], eigvec[1, :])[1]*180/np.pi

        # rotate
        self.img = self.img.rotate(angle)

    def get_header_data(self):
        return np.array(self.img.crop(self.header))

    def get_left_upper_bbox_header(self, tresh=60):
        """Get the left upper coordinate of the bounding box of the header

        Parameters
        ----------
        tresh : int, optional
            All pixels lower than the treshold are supposed to be black.
        """
        data = self.get_header_data()
        crop = np.where(data > tresh, 0, 1)

        left = np.where(np.any(crop, axis=0))[0][0]
        upper = np.where(np.any(crop, axis=1))[0][0]

        return left, upper

    def shift(self, left_h, upper_h):
        """Shift the image according to the first form

        Compare the bounding box of the header with the one from the first form
        and shift the image.

        Parameters
        ----------
        left_h, upper_h : int
            The coordinates of the left upper corner of the bounding box of
            the header to which the one of this form is aligned.
        """
        left, upper = self.get_left_upper_bbox_header()
        self.img = self.img.transform(
                        self.img.size, Image.AFFINE,
                        (1, 0, left-left_h, 0, 1, upper-upper_h))

    def init_questions(self):
        """Create all boxes for the questions of this form"""
        self.boxes = [q.generate_boxes(self.img) for q in self.questions]

    def check_positions(self):
        """Mark all positions of the boxes in the image.

        Returns
        -------
        object
            The copy of the Image instance where all boxes are marked as
            rectangles.
        """
        img = self.img.copy()

        for boxes in self.boxes:
            for b in boxes:
                b.mark_position(img)

        return img

    def get_answers(self):
        """Find all answers to the questions.

        Returns
        -------
        tuple
            The first element is the list of answers. For every question the
            status of the box is given. The second element is a dictionary
            of the errors which occured in the analysis of the boxes.
        """
        answers = []
        errors = {}

        for i, (q, boxes) in enumerate(zip(self.questions, self.boxes)):
            ans, error = q.get_answers(boxes)
            answers.append(ans)
            if error:
                errors[i] = error

        return answers, errors
