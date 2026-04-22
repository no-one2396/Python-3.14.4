import cv2 as cv
import os
import numpy as np
from matplotlib import pyplot as plt
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import *
from PIL import Image, ImageTk

root = Tk()

def affline_set():
    return

def get_image():
    if (url_path.get() is not None and os.path.isfile(url_path.get())):
        file_path = url_path
    else:
        file_path = filedialog.askopenfilename(parent=root,
                                      initialdir=os.path.dirname(__file__),
                                      title="Select A File",
                                      filetypes = (("Image files", "*.jpg *.png *.gif"), ("All files", "*")))
    if (file_path is not None):
        file_name = os.path.basename(file_path)
        original_image = Image.open(file_path)
        x, y = original_image.size
        width.set(x)
        height.set(y)
        img_type = original_image.format
        bit_depth = original_image.mode
        if (width.get() > 960 and height.get() > 540):
            resized_image = original_image.resize((960, 540))
        elif (width.get() < 960 and height.get() < 540):
            resized_image = original_image
        else:
            print("Image is too big width = {width} and hieght = {hieght} which should be below 960, 940")
        reheight, rewidth = resized_image.size
        tk_image = ImageTk.PhotoImage(resized_image)
        image_label.configure(image=tk_image)
        image_label.image= tk_image
        image_label.grid(padx=20, pady=20)
        current = info_title.cget("text")
        info_title.configure(text=current + file_name)
        current = info_resize.cget("text")
        info_resize.configure(text=current + str(rewidth) + ", " + str(reheight))
        current = info_size.cget("text")
        info_size.configure(text=current + str(width.get()) + ", " + str(height.get()))
        current = info_bit.cget("text")
        info_bit.configure(text=current + bit_depth)
        current = info_type.cget("text")
        info_type.configure(text=current + img_type)
        offset_x.configure(from_=-width.get(), to_=width.get())
        offset_y.configure(from_=-height.get(), to_=height.get())
        rot_x.configure(from_=-width.get(), to_=width.get())
        rot_y.configure(from_=-height.get(), to_=height.get())


Tree_Object = {
"RETR_EXTERNAL": cv.RETR_EXTERNAL,
"RETR_TREE": cv.RETR_TREE,
"CHAIN_APPROX_NONE": cv.CHAIN_APPROX_NONE,
"CHAIN_APPROX_SIMPLE": cv.CHAIN_APPROX_SIMPLE,
"CHAIN_APPROX_TC89_L1": cv.CHAIN_APPROX_TC89_L1,
"CHAIN_APPROX_TC89_KCOS": cv.CHAIN_APPROX_TC89_KCOS,
"THRESH_BINARY": cv.THRESH_BINARY,
"THRESH_BINARY_INV": cv.THRESH_BINARY_INV,
"THRESH_TRUNC": cv.THRESH_TRUNC,
"THRESH_TOZERO": cv.THRESH_TOZERO,
"THRESH_TOZERO_INV": cv.THRESH_TOZERO_INV,
"THRESH_MASK": cv.THRESH_MASK,
"ADAPTIVE_THRESH_MEAN_C": cv.ADAPTIVE_THRESH_MEAN_C,
"ADAPTIVE_THRESH_GAUSSIAN_C": cv.ADAPTIVE_THRESH_GAUSSIAN_C,
"INTER_NEAREST": cv.INTER_NEAREST,
"INTER_LINEAR": cv.INTER_LINEAR,
"INTER_CUBIC": cv.INTER_CUBIC,
"INTER_AREA": cv.INTER_AREA,
"INTER_LANCZOS4": cv.INTER_LANCZOS4,
"INTER_LINEAR_EXACT": cv.INTER_LINEAR_EXACT,
"INTER_NEAREST_EXACT": cv.INTER_NEAREST_EXACT,
"INTER_MAX": cv.INTER_MAX,
"WARP_FILL_OUTLIERS": cv.WARP_FILL_OUTLIERS,
"WARP_INVERSE_MAP": cv.WARP_INVERSE_MAP,
"WARP_RELATIVE_MAP": cv.WARP_RELATIVE_MAP,
"THRESH_OTSU": cv.THRESH_OTSU,
"THRESH_TRIANGLE": cv.THRESH_TRIANGLE,
"THRESH_DRYRUN": cv.THRESH_DRYRUN
}
contour_retrieval_modes = [
"RETR_LIST",
"RETR_TREE",
"RETR_CCOMP",
"RETR_FLOODFILL",
"RETR_EXTERNAL"
]
image_transforms = [
"INTER_NEAREST",
"INTER_LINEAR",
"INTER_CUBIC",
"INTER_AREA",
"INTER_LANCZOS4",
"INTER_LINEAR_EXACT",
"INTER_NEAREST_EXACT",
"INTER_MAX",
"WARP_FILL_OUTLIERS",
"WARP_INVERSE_MAP",
"WARP_RELATIVE_MAP",
]

approximation_modes = [
"CHAIN_APPROX_NONE",
"CHAIN_APPROX_SIMPLE"
"CHAIN_APPROX_TC89_L1",
"CHAIN_APPROX_TC89_KCOS"
]

primary_threshhold = [
"THRESH_BINARY",
"THRESH_BINARY_INV",
"THRESH_TRUNC",
"THRESH_TOZERO",
"THRESH_TOZERO_INV",
"THRESH_MASK"
]

flagged_threshhold = [
"THRESH_OTSU",
"THRESH_TRIANGLE",
"THRESH_DRYRUN"
]

adaptive_threshhold = [
"ADAPTIVE_THRESH_MEAN_C",
"ADAPTIVE_THRESH_GAUSSIAN_C"
]

shift_transform =[
"Left Top Down",
"Left Top Up",
"Right Top Down",
"Right Top Up",
"Left Bottom Down",
"Left Bottom Up",
"Right Bottom Down",
"Right Bottom Up",
]

third_option = [
"Edges",
"Threshold"
]

fifth_option = [
"Adaptive",
"Basic"
]

seventh_option = [
"Canny",
"Threshhold"
]

main_frame = Frame(root, width=400, height=500, bg="lightblue", bd=2, relief="sunken")
main_frame.grid(row = 0, column = 0, rowspan = 3, columnspan = 2, sticky = W+E+N+S, padx=5, pady=5) 
info_frame = Frame(root, width=400, height=500, bg="lightblue", bd=2, relief="sunken")
info_frame.grid(row = 3, column = 0, rowspan = 3, columnspan = 2, sticky = W+E+N+S, padx=5, pady=5)
image_frame = Frame(root, width=400, height=500, bg="lightblue", bd=2, relief="sunken")
image_frame.grid(row = 0, column = 2, rowspan = 6, columnspan = 3, sticky = W+E+N+S, padx=5, pady=5)

tabControl = ttk.Notebook(main_frame)
image_tab = ttk.Frame(tabControl)
operation_tab = ttk.Frame(tabControl)
advanced_tab = ttk.Frame(tabControl)
tabControl.add(image_tab, text='Image Details')
tabControl.add(operation_tab, text='Basic Operation')
tabControl.add(advanced_tab, text='Advanced Operation')

width = IntVar(root)
height = IntVar(root)
affine_direction = StringVar(root)
affine_direction.set(shift_transform[0])
seventh = StringVar(root)
seventh.set(seventh_option[0])
contour_mode = tk.StringVar()
contour_mode.set(contour_retrieval_modes[0])
fifth = tk.StringVar()
fifth.set(fifth_option[0])

combo = ttk.Combobox(operation_tab, textvariable=contour_mode, values=contour_retrieval_modes)
minimum = tk.Scale(operation_tab, from_=0, to_=255, orient='horizontal', length= 200, label="minimum")
maximum = tk.Scale(operation_tab, from_=0, to=255, orient='horizontal', length= 200, label="maximum")
entry = tk.Scale(operation_tab, from_=0, to=12, orient='horizontal', length= 48, label="defects")
combo.grid(row=0, column=0, columnspan=2, sticky="ew", pady=10)
minimum.grid(row=1, column=0, columnspan=2, sticky="nsew")
maximum.grid(row=2, column=0, columnspan=2, sticky="nsew")
entry.grid(row=3, column=0, columnspan=2, sticky="nsew")

url_path = tk.Entry(image_tab, text="", font=("Arial", 8, "bold"), relief="sunken", bg="white")
url_path.grid(row=0, column=0, columnspan=2, sticky="ew")
tk.Button(image_tab, text="...", command=get_image, width=5).grid(row=0, column=2, sticky="ew")
tabControl.pack(expand=1, fill="both")
resized_image = Image.new('RGB', (960, 540), color="lightblue")
tk_image = ImageTk.PhotoImage(resized_image)
image_label = tk.Label(image_frame, image=tk_image, borderwidth=0, highlightthickness=0)
image_label.image= tk_image
info_title = tk.Label(image_tab, text="title: ", font=("Arial", 16), anchor="w", justify="left", padx=5)
info_resize = tk.Label(image_tab, text="resize: ", font=("Arial", 16), anchor="w", justify="left", padx=5)
info_size = tk.Label(image_tab, text="original: ", font=("Arial", 16), anchor="w", justify="left", padx=5)
info_bit = tk.Label(image_tab, text="bit: ", font=("Arial", 16), anchor="w", justify="left", padx=5)
info_type = tk.Label(image_tab, text="file type: ", font=("Arial", 16), anchor="w", justify="left", padx=5)
tk.Label(image_tab, text="Transform Image:", font=("Arial", 16), anchor="w", justify="left", padx=5).grid(row=6, column=0, columnspan=2, sticky="ew")
rotation_x = tk.Scale(image_tab, from_=0, to=100, orient='horizontal', length= 200, label="x rotation position")
rotation_y = tk.Scale(image_tab, from_=0, to=100, orient='horizontal', length= 200, label="y rotation position")
tk.Label(image_tab, text="translation of x", anchor="w", justify="left", padx=5).grid(row=8, column=0, sticky="ew")
tk.Label(image_tab, text="translation of y", anchor="w", justify="left", padx=5).grid(row=8, column=1, columnspan=2, sticky="ew")
offset_x = ttk.Spinbox(image_tab, from_=0, to=100)
offset_y = ttk.Spinbox(image_tab, from_=0, to=100)
tk.Label(image_tab, text="rotation of x", anchor="w", justify="left", padx=5).grid(row=10, column=0, sticky="ew")
tk.Label(image_tab, text="rotation of y", anchor="w", justify="left", padx=5).grid(row=10, column=1, columnspan=2, sticky="ew")
rot_x = ttk.Spinbox(image_tab, from_=0, to=100)
rot_y = ttk.Spinbox(image_tab, from_=0, to=100)
rotation = tk.Scale(image_tab, from_=0, to=359, orient='horizontal', length= 200, label="rotation angle in degrees").grid(row=12, column=0, columnspan=4, sticky="ew")
tk.Label(image_tab, text="manual deformation affline", anchor="w", justify="left", padx=5).grid(row=13, column=0, columnspan=4, sticky="ew")
affine_transform = ttk.Combobox(image_tab, textvariable=affine_direction, values=shift_transform, command=affline_set).grid(row=14, column=0, sticky="ew")
affline_pt1 = tk.Entry(image_tab, text="", font=("Arial", 8, "bold"), relief="sunken", bg="white").grid(row=14, column=1, sticky="w")
affline_pt2 = tk.Entry(image_tab, text="", font=("Arial", 8, "bold"), relief="sunken", bg="white").grid(row=14, column=2, sticky="w")
info_title.grid(row=1, column=0, columnspan=2, sticky="ew")
info_resize.grid(row=2, column=0, columnspan=2, sticky="ew")
info_size.grid(row=3, column=0, columnspan=2, sticky="ew")
info_bit.grid(row=4, column=0, columnspan=2, sticky="ew")
info_type.grid(row=5, column=0, columnspan=2, sticky="ew")
rotation_x.grid(row=7, column=0, sticky="ew")
rotation_y.grid(row=7, column=1, columnspan=2, sticky="ew")
offset_x.grid(row=9, column=0, sticky="ew")
offset_y.grid(row=9, column=1, columnspan=2, sticky="ew")
rot_x.grid(row=11, column=0, sticky="ew")
rot_y.grid(row=11, column=1, columnspan=2, sticky="ew")
image_label.grid(padx=20, pady=20)

root.mainloop()
