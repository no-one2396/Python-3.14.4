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
"THRESH_BINARY": cv.THRESH_BINARY,
"THRESH_BINARY_INV": cv.THRESH_BINARY_INV,
"THRESH_TRUNC": cv.THRESH_TRUNC,
"THRESH_TOZERO": cv.THRESH_TOZERO,
"THRESH_TOZERO_INV": cv.THRESH_TOZERO_INV,
"ADAPTIVE_THRESH_MEAN_C": cv.ADAPTIVE_THRESH_MEAN_C,
"ADAPTIVE_THRESH_GAUSSIAN_C": cv.ADAPTIVE_THRESH_GAUSSIAN_C
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
"Threshold"
]
fourth_option = [
"ADAPTIVE_THRESH_MEAN_C",
"ADAPTIVE_THRESH_GAUSSIAN_C"
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
seventh_option = [
"Canny",
"Threshhold"
]

def show_value():
    print(f"Slider Value: {minimum.get()}")
    print(f"Slider Value: {maximum.get()}")
    print(f"contour_options: {entry.get()}")
    print(f"Slider Value: {fifth.get()}") #thresh
    print(f"Slider Value: {sixth.get()}") #combo
    print(f"image size: {seventh.get()}") #contour
    return
    img = cv.imread(file_path)
    resized_img = cv.resize(img, (960, 540))
    gray_image = cv.cvtColor(resized_img, cv.COLOR_BGR2GRAY)
    median_val = np.median(gray_image)
    lower_val = int(minimum.get() * 2.55)  # 76
    upper_val = int(maximum.get() * 2.55)  # 178
    edges = ""
    if (seventh.get() == "Canny"):
        edges = cv.Canny(gray_image,lower_val,upper_val)
    elif (seventh.get() == "Threshhold"):
        if (fifth.get() == "Basic"):
            ret, edges = cv.threshold(gray_image,lower_val,upper_val, 0)
        elif (fifth.get() == "Adaptive"):
            edges = cv.adaptiveThreshold(gray_image,upper_val, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY,11,2)
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

def thresh_desired():
    if (seventh.get() == "Canny"):
        for option in thresh:
            option.config(state="disabled")
            option.deselect() 
    else:
        for option in thresh:
            option.config(state="normal")
    option_changed()

def option_changed():
    if (seventh.get() == "Threshhold"):
        if (fifth.get() == "Adaptive"):
            combo['values'] = fourth_option
            sixth.set(fourth_option[0])
        else:
            combo['values'] = sixth_option
            sixth.set(sixth_option[0])
        #minimum and maximum values derived from average 8bit images update where necessary
        minimum.configure(from_=0, to_=50)
        maximum.configure(from_=0, to_=200)
    else:
        combo['values'] = first_option
        sixth.set(first_option[0])
        minimum.configure(from_=0, to_=255)
        maximum.configure(from_=0, to_=255)
    return

# Create a frame with a border and background color
main_frame = Frame(root, width=400, height=500, bg="lightblue", bd=2, relief="sunken")
main_frame.grid(row = 0, column = 0, rowspan = 3, columnspan = 2, sticky = W+E+N+S, padx=5, pady=5) 
info_frame = Frame(root, width=400, height=500, bg="lightblue", bd=2, relief="sunken")
info_frame.grid(row = 3, column = 0, rowspan = 3, columnspan = 2, sticky = W+E+N+S, padx=5, pady=5)
image_frame = Frame(root, width=400, height=500, bg="lightblue", bd=2, relief="sunken")
image_frame.grid(row = 0, column = 2, rowspan = 6, columnspan = 3, sticky = W+E+N+S, padx=5, pady=5)

# Add a label inside the frame
seventh = StringVar(root)
seventh.set(seventh_option[0])
sixth = tk.StringVar()
sixth.set(first_option[0])
fifth = tk.StringVar()
fifth.set(fifth_option[0])
label = tk.Label(main_frame, text="Select contour search type:", bg="lightblue")
label.grid(row=0, column=0, columnspan=2, sticky="nsew")
for x, option in enumerate(seventh_option):
    contour_options = tk.Radiobutton(main_frame, 
              indicatoron = 0,
              width = 15,
              text= option,
              variable = seventh,
              value=option,
              command=thresh_desired)
    if (x == 0):
        contour_options.grid(row=1, column=0, sticky="nsew", ipadx=5, ipady=5)
    else:
        contour_options.grid(row=1, column=1, sticky="nsew", ipadx=5, ipady=5)
thresh = []
for x, option in enumerate(fifth_option):
    thresh_options = tk.Radiobutton(main_frame, 
              indicatoron = 0,
              width = 10,
              text= option,
              variable = fifth,
              value=option,
              command=option_changed)
    if (x == 0):
        thresh_options.grid(row=2, column=0, sticky="nsew", ipadx=5, ipady=5)
    else:
        thresh_options.grid(row=2, column=1, sticky="nsew", ipadx=5, ipady=5)
    thresh_options.deselect() 
    thresh.append(thresh_options)
combo = ttk.Combobox(main_frame, textvariable=sixth, values=first_option)
minimum = tk.Scale(main_frame, from_=0, to_=255, orient='horizontal', length= 200, label="minimum")
maximum = tk.Scale(main_frame, from_=0, to=255, orient='horizontal', length= 200, label="maximum")
entry = tk.Scale(main_frame, from_=0, to=12, orient='horizontal', length= 48, label="defects")
tk.Button(main_frame, text="Get Value", command=show_value).grid(row=9, column=0, columnspan=2, sticky="nsew", ipadx=10, ipady=10)
info_title = tk.Label(info_frame, text="title: " + file_name, font=("Arial", 16, "bold"), bg="lightblue")
info_resize = tk.Label(info_frame, text="resize: " + str(reheight) + " " + str(rewidth), font=("Arial", 16, "bold"), bg="lightblue")
info_size = tk.Label(info_frame, text="original: " + str(height) + " " + str(width), font=("Arial", 16, "bold"), bg="lightblue")
info_bit = tk.Label(info_frame, text="bit: " + str(bit_depth), font=("Arial", 16, "bold"), bg="lightblue")
info_type = tk.Label(info_frame, text="file type: " + img_type, font=("Arial", 16, "bold"), bg="lightblue")
build_info = tk.Entry(info_frame, text="code build info:", font=("Arial", 10, "bold"), relief="flat", readonlybackground=info_frame.cget("bg"), bg="lightblue")
build_info.insert(0, "code build info:")
build_info.configure(state="readonly") 
info_title.grid(row=0, column=0, columnspan=2, sticky="ew")
info_resize.grid(row=1, column=0, columnspan=2, sticky="ew")
info_size.grid(row=2, column=0, columnspan=2, sticky="ew")
info_bit.grid(row=3, column=0, columnspan=2, sticky="ew")
info_type.grid(row=4, column=0, columnspan=2, sticky="ew")
build_info.grid(row=5, column=0, columnspan= 3, sticky="ew")
combo.grid(row=3, column=0, rowspan=2, columnspan=2, sticky="ew")
minimum.grid(row=5, column=0, columnspan=2, sticky="nsew")
maximum.grid(row=6, column=0, columnspan=2, sticky="nsew")
entry.grid(row=7, column=0, columnspan=2, sticky="nsew")
tk_image = ImageTk.PhotoImage(resized_image)
image_label = tk.Label(image_frame, image=tk_image, borderwidth=0, highlightthickness=0)
image_label.image= tk_image
image_label.grid(padx=20, pady=20)

thresh_desired()
root.mainloop()
