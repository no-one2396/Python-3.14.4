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
root.wm_attributes('-topmost', 1)
root.withdraw()
file_path = filedialog.askopenfilename(parent=root,
                              initialdir=os.path.dirname(__file__),
                              title="Select A File",
                              filetypes = (("Image files", "*.jpg *.png *.gif"), ("All files", "*")))
file_name = os.path.basename(file_path)
root.deiconify()
original_image = Image.open(file_path)
width, height = original_image.size
img_type = original_image.format
bit_depth = original_image.mode
resized_image = original_image.resize((960, 540))
reheight, rewidth = resized_image.size


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
label = ttk.Label(image_tab, text="This is inside Tab 1")
label.pack(padx=10, pady=10)
tabControl.pack(expand=1, fill="both")
root.mainloop()
