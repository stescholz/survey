from __future__ import division

import numpy as np
from PIL import ImageDraw


class Box:
    """A box in a form which can be checked

    Parameters
    ---------
    length : int
        The length of the surrounding box in pixel. (static)
    length_box : int
        The length of the box in pixel. (static)
    length_exterior : int
        The length of the exterior box in pixel. (static)
    center : tuple
        The coordinates of the center of the box before moving.
    left, upper : int
        The coordinates of the left upper corner of the box with respect to the
        form.
    data : array, shape(length, length)
        The grayscale (0-255) values for each pixel.

    Attributes
    ----------
    center_left, center_upper: int
        The coordinates of the center of the box with respect to the form.
    img: object
        The Image instance of the form.
    """
    length = 30
    length_box = 24
    length_exterior = 44

    def __init__(self, center_left, center_upper, img):

        self.center = center_left, center_upper

        # first crop a bigger box from the form
        self.left = center_left - Box.length_exterior//2
        self.upper = center_upper - Box.length_exterior//2

        crop = img.crop((self.left,
                         self.upper,
                         self.left+Box.length_exterior,
                         self.upper+Box.length_exterior))

        # find the corner of the box in the bigger box and adjust the coords
        corner_left, corner_upper = self.find_left_upper_corner(crop)
        self.left += corner_left - (Box.length-Box.length_box)//2
        self.upper += corner_upper - (Box.length-Box.length_box)//2

        # crop the box from the image and create an array
        self.data = np.array(img.crop((self.left,
                                       self.upper,
                                       self.left+Box.length,
                                       self.upper+Box.length)))

    def find_left_upper_corner(self, crop_img, tresh=100):
        """Find the real left upper corner of the box in the image

        Approximate the real left upper corner of the box in the image
        because the forms are usally scanned and you can not perfectly fit
        the coordinates for each box for the whole survey.

        Parameters
        ----------
        crop_img: object
            The Image instance of a surrounding box.
        tresh: int, optional
            Above this treshold every pixel is supposed to be white and all
            other are supposed to be black.

        Returns
        -------
        tupel of ints
            The left upper corner of the box with respected to crop_img.

        """
        data = np.where(np.array(crop_img) > tresh, 0, 1)
        width, height = crop_img.size

        max_val = 0
        left, upper = 0, 0
        # find the maximum of the sum an L-like snippet in crop_img.
        for l in np.argsort(np.sum(data[:, :width], axis=0))[-5:][::-1]:
            for u in np.argsort(np.sum(data[:height//2, :],
                                       axis=1))[-5:][::-1]:
                val = (np.sum(data[u:u+Box.length_box, l]) +
                       np.sum(data[u, l:l+Box.length_box]))
                if val > max_val:
                    max_val = val
                    left, upper = l, u

        return left, upper

    def mark_position(self, img, color=0, lw=4, original=False):
        """Draw the position of the box in an image.

        Parameters
        ----------
        img : object
            The Image instance of the form.
        color : int, optional
            The color of the box in the image.
        lw : int, optional
            The line width of the rectangle.
        original : boolean, optional
            Use the orignal position of the center or the calculated.
        """

        if original:
            left = self.center[0] - Box.length//2
            upper = self.center[1] - Box.length//2
        else:
            left = self.left
            upper = self.upper

        draw = ImageDraw.Draw(img)
        for i in range(lw):
            draw.rectangle([(left+i, upper+i),
                            (left+Box.length-i, upper+Box.length-i)],
                           outline=color)
        del draw

    def mean(self):
        """Compute the mean of the pixels.

        Returns
        -------
        float
            The mean of the pixels.
        """
        return np.mean(self.data)
