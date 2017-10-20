import numpy as np
from PIL import Image, ImageDraw


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

    def rotate(self, tresh=60, method="rect"):
        """Rotate the form to correct the skew after scanning

        Parameters
        ----------
        tresh : int, optional
            All pixels lower than the treshold are supposed to be black.
        method : str, optional
            The method to find the angle of the rotation. "pca" does a PCA
            and "rect" tries to find the upper edge of the rectangle in the
            header.
        """
        # extract header and do a pca to find the rotation angle
        data = self.get_header_data()

        if method == "pca":
            x, y = np.where(data < tresh)
            eigval, eigvec = np.linalg.eigh(np.cov(np.array([x, y])))
            angle = np.arctan2(eigvec[0, :], eigvec[1, :])[1]*180/np.pi

        elif method == "rect":

            data = np.where(data < tresh, 1, 0)
            y, x = np.nonzero(data)

            data = data[y.min():y.max()+1, x.min():x.max()+1]
            width = data.shape[1]

            p1 = np.nonzero(data[0, :])[0][0], 0

            if p1[0] < width/2:
                y, x = np.nonzero(data[:20, -10:])
                p2 = width-10+x[0], y[0]
            else:
                p2 = p1
                y, x = np.nonzero(data[:20, :10])
                p1 = x[0], y[0]

            angle = np.arctan2(p2[1]-p1[1], p2[0]-p1[0])*180/np.pi

        else:
            raise NotImplementedError("method not implemented")

        # rotate
        self.img = self.img.rotate(angle)

    def get_header_data(self):
        return np.array(self.img.crop(self.header))

    def get_left_upper_bbox_header(self, tresh=40):
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

    def check_positions(self, original=False):
        """Mark all positions of the boxes and the header in the image.

        Parameters
        ----------
        original : boolean, optional
            Use the orignal position of the center or the calculated.

        Returns
        -------
        object
            The copy of the Image instance where all boxes and the header are
            marked as rectangles.
        """
        img = self.img.copy()

        draw = ImageDraw.Draw(img)
        draw.rectangle(self.header, outline=0)

        for boxes in self.boxes:
            for b in boxes:
                b.mark_position(img, original=original)

        return img

    def get_answers(self, lower=115, upper=208, full=False):
        """Find all answers to the questions.

        Parameters
        ----------
        lower, upper : int, optional
            The treshold for the mean of the pixels of the box. If the mean is
            between the upper and lower bound the box should be checked
            otherwise not.
        full : boolean, optional
            If true, the status of every box of the question is returned.
            Otherwise only the answer is given.

        Returns
        -------
        tuple
            The first element is the list of answers. According to the
            parameter for every question the status of all the boxes is given
            or only the answer. The second element is a dictionary of the
            errors which occured in the analysis of the boxes.
        """
        answers = []
        errors = {}

        for i, (q, boxes) in enumerate(zip(self.questions, self.boxes)):
            ans, error = q.get_answers(boxes, lower, upper, full)
            answers.append(ans)
            if error:
                errors[i] = error

        return answers, errors
