import cv2 as cv
import os
import numpy as np
from matplotlib import pyplot as plt
import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import Image, ImageTk

root = tk.Tk()
root.wm_attributes('-topmost', 1)
root.withdraw()
file_path = filedialog.askopenfilename(parent=root,
                              initialdir=os.path.dirname(__file__),
                              title="Select A File",
                              filetypes = (("Image files", "*.jpg *.png *.gif"), ("All files", "*")))
root.deiconify()

label = tk.Label(root, text="Hello, GUI!")

def show_value():
    print(f"Slider Value: {minimum.get()}")
    print(f"Slider Value: {Maximum.get()}")
    print(f"image size: {resized_image.size}")
    img = cv.imread(file_path)
    resized_img = cv.resize(img, (960, 540))
    gray_image = cv.cvtColor(resized_img, cv.COLOR_BGR2GRAY)
    median_val = np.median(gray_image)
    lower_val = int(minimum.get() * 2.55)  # 76
    upper_val = int(Maximum.get() * 2.55)  # 178
    edges = cv.Canny(gray_image,lower_val,upper_val)
    ret, thresh = cv.threshold(gray_image, 127, 255, 0)
    contours, hierarchy = cv.findContours(edges, Tree_Object[first.get()], Tree_Object[second.get()])
    if len(contours) > 0:
        for con in contours:
            hull = cv.convexHull(con,returnPoints = False)
            hull = np.sort(hull, axis=0)[::-1]
            defects = cv.convexityDefects(con,hull)
            print(f"{con} : countour")
            print(f"{defects} : defects")
            if (defects is not None):
                print(f"{len(defects)}")
                if (len(defects) > entry.get()):
                    for i in range(defects.shape[0]):
                        s,e,f,d = defects[i,0]
                        start = tuple(con[s][0])
                        end = tuple(con[e][0])
                        this_y = end[1]
                        far = tuple(con[f][0])
                        this_far_y = far[1]
                        cv.line(resized_img,start,end,[0,255,0],2)
                        cv.circle(resized_img,far,5,[0,0,255],-1)
                    print(f"{start} start : {end} end \n {far} far : {hull} hull \n {this_y} : {this_far_y}")
        cv_img_rgb = cv.cvtColor(resized_img, cv.COLOR_BGR2RGB)
        pil_img = Image.fromarray(cv_img_rgb)
        tk_img = ImageTk.PhotoImage(image=pil_img)
        image_label.configure(image=tk_img)
        image_label.image = tk_img
        print("User selected:", first.get())

original_image = Image.open(file_path)
resized_image = original_image.resize((960, 540))
height, width = resized_image.size
width+= 300
height+= 100
Tree_Object = {
"RETR_EXTERNAL": cv.RETR_EXTERNAL,
"RETR_TREE": cv.RETR_TREE,
"CHAIN_APPROX_NONE": cv.CHAIN_APPROX_NONE,
"CHAIN_APPROX_SIMPLE": cv.CHAIN_APPROX_SIMPLE,
"THRESH_BINARY": cv.THRESH_BINARY,
"THRESH_BINARY_INV": cv.THRESH_BINARY_INV,
"THRESH_TRUNC": cv.THRESH_TRUNC,
"THRESH_TOZERO": cv.THRESH_TOZERO,
"THRESH_TOZERO_INV": cv.THRESH_TOZERO_INV
}
first_option = [
"RETR_EXTERNAL",
"RETR_TREE"
]
second_option = [
"CHAIN_APPROX_NONE",
"CHAIN_APPROX_SIMPLE"
]
third_option = [
"Edges",
"Threshold value"
]
fifth_option = [
"Adaptive",
"Basic"
]
sixth_option = [
"THRESH_BINARY",
"THRESH_BINARY_INV",
"THRESH_TRUNC",
"THRESH_TOZERO",
"THRESH_TOZERO_INV"
]
first = StringVar(root)
first.set(first_options[0]) # default value
second = StringVar(root)
second.set(second_options[0]) # default value
root.geometry(f"{height}x{width}")
tk_image = ImageTk.PhotoImage(resized_image)
minimum = tk.Scale(root, from_=0, to_=100, orient='horizontal', length= 200)
Maximum = tk.Scale(root, from_=0, to=100, orient='horizontal', length= 200)
entry = tk.Scale(root, from_=0, to=12, orient='horizontal', length= 48)
contour_one = OptionMenu(root, first, *first_options)
contour_two = OptionMenu(root, second, *second_options)
tk.Button(root, text="Get Value", command=show_value).pack()
minimum.pack(pady=10)
Maximum.pack(pady=10)
contour_one.pack(pady=10)
contour_two.pack(pady=10)
entry.pack(pady=10)
image_label = tk.Label(root, image=tk_image)
image_label.pack()
label.pack()

root.mainloop()
