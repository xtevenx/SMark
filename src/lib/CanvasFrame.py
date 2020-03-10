# this module is inspired by the following article:
# https://stackoverflow.com/questions/22835289/how-to-get-tkinter-canvas-to-dynamically-resize-to-window-width

from tkinter import Canvas, Frame


class CanvasFrame(Canvas):
    """
    A class consisting of a `tkinter.Frame` object embedded within a
    `tkinter.Canvas` object.

    The purpose of this is to be able to provide a scrollbar to a group
    of widgets. The Canvas object is required to attach a scrollbar
    while the Frame object is required to embed widgets into.
    """

    def __init__(self, parent, **kwargs):
        """
        Initialize the inner `tkinter.Frame` object and set up the
        resizing callback to run on the Canvas' resize.
        """

        super().__init__(parent, **kwargs)

        self.frame = Frame(self, **kwargs)
        self.frame.grid(column=0, row=0, sticky="nsew")

        self.bind("<Configure>", self._resize_callback)

    def _resize_callback(self, event):
        """Callback to be bound to the Canvas' resize."""

        x_scale = event.width / self.frame.winfo_width()
        y_scale = event.height / self.frame.winfo_height()

        self.config(width=event.width, height=event.height)
        self.scale("all", 0, 0, x_scale, y_scale)
