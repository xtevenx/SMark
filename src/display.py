from typing import Optional, Sequence
import statistics

DISPLAY_WIDTH: int = 72

CENTER_FORMAT: str = "| {} |"
LINE_FORMAT: str = "| {left}{right} |"
NUM_FORMAT: str = "{:.2f}"


# Headers display -----------------------------------------------------

def display_header(header: str) -> None:
    print(f"-> {header} <-".center(DISPLAY_WIDTH, "-"))


# Data Statistics display ---------------------------------------------

def display_info(
        scores: Sequence[float],
        header: Optional[str] = None,
        total_score: Optional[float] = None
) -> None:
    """Display a box of statistics about a set of scores.

    Displays a formatted message box describing the maximum, minimum,
    arithmetic mean, and standard deviation for both the scores and
    percentages, along with a header at the top.

    For example, if the function was called as such::

        display_info([10, 14, 20, 7, 13, 11, 9, 11],
                     header="Some random stats", total_score=20)

    the following will be outputted::

        ------------------------------------------------------------------------
        |                          SOME RANDOM STATS                           |
        |                                                                      |
        | Maximum score:                                                 20.00 |
        | Minimum score:                                                  7.00 |
        | Average (mean) score:                                          11.88 |
        | Scores standard deviation:                                      3.94 |
        |                                                                      |
        | Maximum percentage:                                          100.00% |
        | Minimum percentage:                                           35.00% |
        | Average (mean) percentage:                                    59.38% |
        | Percentages standard deviation:                               19.72% |
        ------------------------------------------------------------------------

    :param scores: A sequence of floats representing the set of scores for
        which to display the statistics for.
    :param header: The header which is to be displayed at the top fo the box.
        If this is None, the title is not displayed.
    :param total_score: A float representing the total possible score. If this
        is None, the statistics of percentages are not displayed.
    """

    percents = tuple(n * 100 / total_score for n in scores)

    print("-" * DISPLAY_WIDTH)

    if header is not None:
        print(_format_center(header.upper()))
        print(_format_line())

    print(_format_line("Maximum score:", NUM_FORMAT.format(max(scores))))
    print(_format_line("Minimum score:", NUM_FORMAT.format(min(scores))))

    print(_format_line(
        "Average (mean) score:", NUM_FORMAT.format(statistics.mean(scores))))
    print(_format_line(
        "Scores standard deviation:", NUM_FORMAT.format(statistics.stdev(scores))))

    if total_score is not None:
        print(_format_line())

        print(_format_line(
            "Maximum percentage:", f"{NUM_FORMAT.format(max(percents))}%"))
        print(_format_line(
            "Minimum percentage:", f"{NUM_FORMAT.format(min(percents))}%"))

        print(_format_line(
            "Average (mean) percentage:",
            f"{NUM_FORMAT.format(statistics.mean(percents))}%"))
        print(_format_line(
            "Percentages standard deviation:",
            f"{NUM_FORMAT.format(statistics.stdev(percents))}%"))

    print("-" * DISPLAY_WIDTH)


def _format_center(text: str) -> str:
    no_text = CENTER_FORMAT.format("")
    text = text.center(DISPLAY_WIDTH - len(no_text))
    return CENTER_FORMAT.format(text)


def _format_line(left_side: str = "", right_side: str = "") -> str:
    left_only = LINE_FORMAT.format(left=left_side, right="")
    right_side = right_side.rjust(DISPLAY_WIDTH - len(left_only))
    return LINE_FORMAT.format(left=left_side, right=right_side)


# Other utility functions ---------------------------------------------

def input_float(prompt: str = "",
                qualifier=lambda v: True,
                qualifier_err: str = "Error: please check that the input is correct."
                ) -> float:
    while val := input(prompt).strip():
        try:
            if qualifier(val := float(val)):
                return val
            print(qualifier_err)
        except ValueError:
            print("Error: could not parse the input.")


# Generate examples for doc-string ------------------------------------

if __name__ == "__main__":
    display_info([10, 14, 20, 7, 13, 11, 9, 11], header="Some random stats", total_score=20)
