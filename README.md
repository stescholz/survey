# survey

Evaluation of a survey by image analysis

## Motivation

I would like to gain some practical experience in data science.

So this project is an exercise for me.

At university we make surveys among our new students to get some idea of the
mathematical skills. In the first lecture we ask them to fill in a form
consisting of multiple choice questions. The task is now to evaluate the survey.

There are about 26 questions and more than 100 sheets. So we scan everything
and analyze the images.

## Preprocessing

After scanning the survey we have a pdf-file containing all forms. We extract
the images with `pdfimages`.

### Skew
After scanning every images is skewed a little bit. This can cause problems when
you try to get the boxes from the images.

Therefore we crop the header of each form and do a principal component analysis
of the black pixels. This gives us a rotation angle to correct the skew.

![rotation](https://user-images.githubusercontent.com/25635571/29772356-b628054a-8bf8-11e7-9f90-97ab7764eae4.png)

In the second version there is a rectangle in the header of the survey. We
seach for the upper edge of this rectangle and correct the skew
according to its position.

### Shift
The next problem when scanning is the shift of each form. Therefore we check
again the header of the form and calculate the bounding box. Every form is then
shifted with respect to the left upper corner of the bounding box of the first
form.

### Boxes
The first steps already lead to good results but we want to improve it. We have
a good idea of the position of each box. In this area we try to find a good a
match for the left und upper line of the box through an analysis of the black
pixels. Then the position of the lines of each boxes differ by a maximum of 2
pixels.

## Analysis
### First try
We take the mean of the pixels in each box. If this is lower than a bound the
box is supposed to be checked and otherwise not (black pixel has value 0 and
white pixel has value 255). This leads already to good results but it is not
easy to get a good bound.
