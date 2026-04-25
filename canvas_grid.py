import cv2 as cv
import os
import numpy as np
from matplotlib import pyplot as plt
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import *
from PIL import Image, ImageTk

root = tk.Tk()
canvas = tk.Canvas(root, width=1800, height=1000, bg="white")
main_frame = tk.Frame(canvas, width=500, height=500, bg="lightblue", bd=2, relief="sunken")
info_frame = tk.Frame(canvas, width=500, height=500, bg="lightblue", bd=2, relief="sunken")
image_frame = tk.Frame(canvas, width=1300, height=1000, bg="lightblue", bd=2, relief="solid")
canvas.grid()
canvas.create_window(0, 0, window=main_frame, anchor="nw")
canvas.create_window(0, 500, window=info_frame, anchor="nw")
canvas.create_window(500, 0, window=image_frame, anchor="nw")
image_canvas = tk.Canvas(image_frame, width=1300, height=1000, bg="white")
step = 40
for x in range(0, 1300, step):
    if (x > 39 and x < 1280):
        image_canvas.create_line(x, 40, x, 960, fill="lightgray")
for y in range(0, 1000, step):
    if (y > 39 and y < 980):
        image_canvas.create_line(40, y, 1260, y, fill="lightgray")
user_layer = Image.new("RGBA", (960, 540), (0, 0, 0, 255))
tk_image = ImageTk.PhotoImage(user_layer)
image_canvas.create_image(100, 200, image=tk_image, anchor="nw")
image_canvas.image = tk_image
image_canvas.grid()
root.mainloop()
