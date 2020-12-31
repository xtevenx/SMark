import statistics

_DISPLAY_WIDTH: int = 72


# Headers display -----------------------------------------------------

def display_header(header: str):
    print(f"-> {header} <-".center(_DISPLAY_WIDTH, "-"))


# Data Statistics display ---------------------------------------------

_CENTER_FORMAT: str = "| {} |"
_LINE_FORMAT: str = "| {left}{right} |"
_NUM_FORMAT = "{:.2f}"


def display_info(data, total_score, header="data statistics"):
    scores = tuple(n * total_score for n in data)
    percents = tuple(n * 100 for n in data)

    print("-" * _DISPLAY_WIDTH)
    print(_format_center(header.upper()))
    print(_format_line())
    print(_format_line("Maximum score:", _NUM_FORMAT.format(max(scores))))
    print(_format_line("Minimum score:", _NUM_FORMAT.format(min(scores))))
    print(_format_line("Average (mean) score:", _NUM_FORMAT.format(statistics.mean(scores))))
    print(_format_line("Scores standard deviation:", _NUM_FORMAT.format(statistics.stdev(scores))))
    print(_format_line())
    print(_format_line("Maximum percentage:", f"{_NUM_FORMAT.format(max(percents))}%"))
    print(_format_line("Minimum percentage:", f"{_NUM_FORMAT.format(min(percents))}%"))
    print(_format_line("Average (mean) percentage:", f"{_NUM_FORMAT.format(statistics.mean(percents))}%"))
    print(_format_line("Percentages standard deviation:", f"{_NUM_FORMAT.format(statistics.stdev(percents))}%"))
    print("-" * _DISPLAY_WIDTH)


def _format_center(text: str) -> str:
    no_text = _CENTER_FORMAT.format("")
    text = text.center(_DISPLAY_WIDTH - len(no_text))
    return _CENTER_FORMAT.format(text)


def _format_line(left_side: str = "", right_side: str = "") -> str:
    left_only = _LINE_FORMAT.format(left=left_side, right="")
    right_side = right_side.rjust(_DISPLAY_WIDTH - len(left_only))
    return _LINE_FORMAT.format(left=left_side, right=right_side)


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
