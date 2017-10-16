import csv
import matplotlib.pyplot as plt
import numpy as np


def transform(data):
    """Prepare the data for plotting

    Parameters
    ----------
    data : list
        A list of tuples. First element is the title of the question and the
        second one is a dictionary which maps the possible answer to the number
        of times the answer was given.
        [("Question1", {"yes":3, "no":4}, ("Question2", {"a":1, "no":2})]

    Returns
    -------
    tuple
        First element is a list of the titles of the questions. Second one is
        a dictionary mapping the possible answer to a list of the quantities
        the answer was given.
        (["Question1", "Question2"], {"yes":[3, 0], "no":[4, 2], "a":[0, 1]})
    """
    questions = [t for t, v in data]
    answers = list(set([k for t, v in data for k in v.keys()]))

    quantities = {}
    for answer in answers:
        quantities[answer] = [v[answer] if answer in v else 0 for t, v in data]

    return questions, quantities


def write_csv(data, fn):
    """Save data for plotting to a csv file

    Transform the data and save to csv file.

    Parameters
    ----------
    data : list
        A list of tuples. First element is the title of the question and the
        second one is a dictionary which maps the possible answer to the number
        of times the answer was given. If there is no title for the answer, the
        key is set to "na".
        [("Question1", {"yes":3, "no":4}, ("Question2", {"a":1, "no":2})]
    fn : str
        The name of the csv file.
    """

    questions, quantities = transform(data)

    if "" in quantities:
        quantities["na"] = quantities[""]
        del quantities[""]

    with open(fn, "w") as csvfile:
        cw = csv.writer(csvfile)
        # header
        cw.writerow(["question"] + quantities.keys())

        for i, question in enumerate(questions):
            cw.writerow([question] + [v[i] for v in quantities.values()])


def write_tex(data, fn):
    r"""Save data for plotting to a tex file

    Create a tex file which contains the data as variables to build a plot.
    For the input
    [("Question1", {"yes":3, "no":4}, ("Question2", {"a b":1, "c  d":2})]
    the file contains
    \newcommand{Question1yes}{3}
    \newcommand{Question1no}{4}
    \newcommand{Question2ab}{1}
    \newcommand{Question2cd}{2}

    Parameters
    ----------
    data : list
        A list of tuples. First element is the title of the question and the
        second one is a dictionary which maps the possible answer to the number
        of times the answer was given. If there is no title for the answer, the
        key is set to "na".
        [("Question1", {"yes":3, "no":4}, ("Question2", {"a":1, "no":2})]
    fn : str
        The name of the tex file.
    """

    with open(fn, "w") as f:
        for title, answers in data:
            for k, v in answers.items():
                if not k:
                    k = "na"
                f.write("\\newcommand{{{}{}}}{{{}}}\n".format(
                                                        title.replace(" ", ""),
                                                        k.replace(" ", ""),
                                                        v))


def create_barplot(data, fn=""):
    """Create a horizontal bar plot

    Parameters
    ----------
    data : list
        A list of tuples. First element is the title of the question and the
        second one is a dictionary which maps the possible answer to the number
        of times the answer was given.
        [("Question1", {"yes":3, "no":4}, ("Question2", {"a":1, "no":2})]
    fn : str, optional
        The name of the filename. If the filename is present, the plot will be
        saved to the file. Otherwise the plot will be displayed.
    """
    questions, quantities = transform(data)

    colors = [plt.cm.Set1(x) for x in np.linspace(0, 1, 9)]

    fig, ax = plt.subplots()
    y_pos = np.arange(len(questions))

    n = len(quantities.keys())
    width = 1./(n+1)

    for i, (k, v) in enumerate(quantities.items()):
        ax.barh(y_pos + i*width, v, width, color=colors[i],
                align="center", label=k if k else "keine Angabe")

    ax.set_yticks(y_pos + (n-1)*0.5*width)
    ax.set_yticklabels(questions)
    ax.set_ylim(-width, len(questions)-1+n*width)
    ax.invert_yaxis()
    ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=n,
              mode="expand", borderaxespad=0.)

    if fn:
        plt.savefig(fn)
    else:
        plt.show()
