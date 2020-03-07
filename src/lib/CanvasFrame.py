# this module is inspired by the following article:
# https://stackoverflow.com/questions/22835289/how-to-get-tkinter-canvas-to-dynamically-resize-to-window-width

from tkinter import Canvas, Frame


class CanvasFrame(Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.frame = Frame(self, **kwargs)
        self.frame.grid(column=0, row=0, sticky="nsew")

        self.bind("<Configure>", self.resize_callback)

    def resize_callback(self, event):
        x_scale = event.width / self.frame.winfo_width()
        y_scale = event.height / self.frame.winfo_height()

        self.config(width=event.width, height=event.height)
        self.scale("all", 0, 0, x_scale, y_scale)
