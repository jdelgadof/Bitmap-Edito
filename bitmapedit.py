import tkinter as tk
from tkinter import ttk


class BitmapEdit(ttk.Frame):
    def __init__(self, parent, bmp, pixels):
        ttk.Frame.__init__(self, parent)
        self.myParent = parent
        self.px = pixels
        self.width = bmp.width
        self.height = bmp.height
        self.bmp = bmp
        self.canvas = None
        self.bits = None
        self.create_grid()

    def create_grid(self):
        self.canvas = tk.Canvas(self,
                                width=self.width * self.px + 1, height=self.height * self.px + 1,
                                borderwidth=0, highlightthickness=0)
        self.bits = [[self.canvas.create_rectangle(c * self.px, r * self.px,
                                                   (c + 1) * self.px, (r + 1) * self.px,
                                                   fill='lightgrey', outline='black')
                      for c in range(self.width)] for r in range(self.height)]
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.click)

    def set_bitmap(self, bmp):
        if bmp.width != self.width or bmp.height != self.height:
            self.width = bmp.width
            self.height = bmp.height
            self.canvas.destroy()
            self.create_grid()
        self.bmp = bmp
        for c in range(self.width):
            for r in range(self.height):
                self.update(c, r)

    def update(self, x, y):
        if self.bmp.get_pixel(x, y):
            self.canvas.itemconfig(self.bits[y][x], fill='black')
        else:
            self.canvas.itemconfig(self.bits[y][x], fill='lightgrey')

    def set_pixel(self, x, y, color):
        self.bmp.set_pixel(x, y, color)
        self.update(x, y)

    def toggle_pixel(self, x, y):
        self.set_pixel(x, y, not self.bmp.get_pixel(x,y))

    def click(self, event):
        c = event.x // self.px
        if c > self.width - 1:
            c = self.width - 1
        r = event.y // self.px
        if r > self.height - 1:
            r = self.height - 1
        self.toggle_pixel(c, r)
