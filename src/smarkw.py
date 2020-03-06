import tkinter as tk
from tkinter.scrolledtext import ScrolledText

from lib.ModifiedMixin import ModifiedMixin

import scale
import stats

# Values are copied from Atom's "One Light" color scheme.
_COLORS = {
    "background": "#F9F9F9",
    "foreground": "#383A42",
    "black": "#000000",
    "red": "#E45649",
    "green": "#50A14F",
    "yellow": "#986801",
    "blue": "#4078F2",
    "purple": "#A626A4",
    "cyan": "#0184BC",
    "white": "#A0A1A7",
    "brightBlack": "#5C6370",
    "brightRed": "#E06C75",
    "brightGreen": "#50A14F",
    "brightYellow": "#986801",
    "brightBlue": "#4078F2",
    "brightPurple": "#A626A4",
    "brightCyan": "#0184BC",
    "brightWhite": "#FFFFFF"
}


class MainWindow(tk.Tk):
    _window_configs = {
        "bg": _COLORS["background"],
    }

    _widget_configs = {
        "bg": _COLORS["background"],
        "font": ("Monaco", 10),
    }

    _label_configs = {
        "font": ("Monaco", 12),
    }

    _input_configs = {}

    _stats_configs = {
        "padx": 10,
    }

    def __init__(self):
        super().__init__()
        self._init()

    def _init(self):
        self._label_configs = {**self._widget_configs, **self._label_configs}
        self._input_configs = {**self._widget_configs, **self._input_configs}
        self._stats_configs = {**self._widget_configs, **self._stats_configs}

        # configure the general window attributes
        self.title("SMark Grade Scale Utility")
        self.configure(self._window_configs)

        self.geometry("720x400")
        self.minsize(width=720, height=400)

        # create the labels
        self.unscaled_label = tk.Label(self, text="Unscaled marks:", **self._label_configs)
        self.unscaled_label.grid(column=0, row=0, columnspan=2, sticky="nsew")

        self.scaled_label = tk.Label(self, text="Scaled marks:", **self._label_configs)
        self.scaled_label.grid(column=2, row=0, columnspan=2, sticky="nsew")

        # create the input and display text boxes
        self.unscaled_input = ResponsiveText(
            self, callback=self.do_scaling, **self._input_configs)
        self.unscaled_input.grid(column=0, row=1, columnspan=2, sticky="nsew")

        self.scaled_display = ScrolledText(self, state="disabled", **self._input_configs)
        self.scaled_display.grid(column=2, row=1, columnspan=2, sticky="nsew")

        # create assignment total input
        self.assignment_total_label = tk.Label(
            self, text="Assignment total:", anchor="w", **self._stats_configs)
        self.assignment_total_label.grid(column=0, row=2, sticky="nsew")

        self.assignment_total = tk.StringVar()
        self.assignment_total.trace("w", lambda *a: self.do_scaling())
        self.assignment_total_input = tk.Entry(
            self, justify=tk.RIGHT, textvariable=self.assignment_total, **self._input_configs)
        self.assignment_total_input.insert(0, "20")
        self.assignment_total_input.grid(column=1, row=2, padx=10, sticky="ew")

        # create unit and copy buttons
        self.use_percentages = tk.BooleanVar()
        self.unit_button = tk.Checkbutton(
            self, text="Display percentages", variable=self.use_percentages, anchor="w",
            command=self.do_scaling, **self._stats_configs)
        self.unit_button.select()
        self.unit_button.grid(column=2, row=2, sticky="nsew")

        self.copy_button = tk.Button(
            self, text="Copy to clipboard", command=self.copy_to_clipboard, **self._stats_configs)
        self.copy_button.grid(column=3, row=2, padx=10, sticky="nsew")

        # create the statistics display labels
        self.unscaled_mean_label = tk.Label(
            self, text="Arithmetic mean:", anchor="w", **self._stats_configs)
        self.unscaled_mean_label.grid(column=0, row=3, sticky="nsew")

        self.unscaled_median_label = tk.Label(
            self, text="Median:", anchor="w", **self._stats_configs)
        self.unscaled_median_label.grid(column=0, row=4, sticky="nsew")

        self.scaled_mean_label = tk.Label(
            self, text="Arithmetic mean (%):", anchor="w", **self._stats_configs)
        self.scaled_mean_label.grid(column=2, row=3, sticky="nsew")

        self.scaled_median_label = tk.Label(
            self, text="Median:", anchor="w", **self._stats_configs)
        self.scaled_median_label.grid(column=2, row=4, sticky="nsew")

        # create the statistics display (and input) boxes
        self.unscaled_mean_display = tk.Label(
            self, text="undefined", anchor="e", **self._stats_configs)
        self.unscaled_mean_display.grid(column=1, row=3, sticky="nsew")

        self.unscaled_median_display = tk.Label(
            self, text="undefined", anchor="e", **self._stats_configs)
        self.unscaled_median_display.grid(column=1, row=4, sticky="nsew")

        self.scaled_mean = tk.StringVar()
        self.scaled_mean.trace("w", lambda *a: self.do_scaling())
        self.scaled_mean_input = tk.Entry(
            self, justify=tk.RIGHT, textvariable=self.scaled_mean, **self._input_configs)
        self.scaled_mean_input.insert(0, "70.0")
        self.scaled_mean_input.grid(column=3, row=3, padx=10, sticky="ew")

        self.scaled_median_display = tk.Label(
            self, text="undefined", anchor="e", **self._stats_configs)
        self.scaled_median_display.grid(column=3, row=4, sticky="nsew")

        # final widget positioning tweaks
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # flag for when finished building init
        self._FINISHED_INIT = True

    def copy_to_clipboard(self):
        scaled_data = self.scaled_display.get("1.0", tk.END).strip()
        self.clipboard_clear()
        self.clipboard_append(scaled_data)

    def do_scaling(self):
        if not hasattr(self, "_FINISHED_INIT"):
            return

        input_data = self.unscaled_input.get("1.0", tk.END).strip()

        try:
            assignment_total = float(self.assignment_total.get())

            input_data = list(float(x) / assignment_total for x in input_data.split())
            assert all(0 <= x <= 1 for x in input_data) and len(input_data) > 0

            scaled_mean = float(self.scaled_mean_input.get()) / 100
            assert 0 <= scaled_mean <= 1
        except (AssertionError, ValueError, ZeroDivisionError):
            self.scaled_display.config(state="normal")
            self.scaled_display.delete("1.0", tk.END)
            self.scaled_display.config(state="disabled")

            self.unscaled_mean_display.config(text="undefined")
            self.unscaled_median_display.config(text="undefined")
            self.scaled_median_display.config(text="undefined")
            return

        scale_foo = (
            scale.inverse_power_scale if stats.mean(input_data) < scaled_mean else
            scale.power_scale
        )
        scaled_data, _ = scale.scale(input_data, scaled_mean, scale_foo)

        self.scaled_display.config(state="normal")
        self.scaled_display.delete("1.0", tk.END)
        self.scaled_display.insert("1.0", "\n".join(
            f"{assignment_total * x:.2f}" for x in scaled_data
        ))
        self.scaled_display.config(state="disabled")

        if self.use_percentages.get():
            self.unscaled_mean_display.config(text=f"{100 * stats.mean(input_data):.2f}%")
            self.unscaled_median_display.config(text=f"{100 * stats.median(input_data):.2f}%")
            self.scaled_median_display.config(text=f"{100 * stats.median(scaled_data):.2f}%")
        else:
            self.unscaled_mean_display.config(
                text=f"{assignment_total * stats.mean(input_data):.1f}")
            self.unscaled_median_display.config(
                text=f"{assignment_total * stats.median(input_data):.1f}")
            self.scaled_median_display.config(
                text=f"{assignment_total * stats.median(scaled_data):.1f}")


class ResponsiveText(ModifiedMixin, ScrolledText):
    def __init__(self, *a, callback=None, **b):
        super().__init__(*a, **b)
        self._init()

        if callback is not None:
            self.been_modified = lambda e: callback()


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
