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
original_image = None
file_path = None

def quadrant_move(self):
    if (file_path is not None):
        img = cv.imread(file_path)
        height,width,ch = img.shape
        point1= [round((width/2)*(quadrant_i.get()/100)),round((height/2)*(quadrant_i.get()/100))]
        point2= [round(width/2+(width/2)*(quadrant_ii.get()/100)),round((height/2-(height/2*quadrant_ii.get()/100)))]
        point3= [round((width/2*quadrant_iii.get()/100)),round(height-(height/2*quadrant_iii.get()/100))]
        point4= [round(width/2+(width/2*quadrant_vi.get()/100)),round(height/2+(height/2*quadrant_vi.get()/100))]
        offset_point= np.float32([[0,0],[width, 0],[0, height],[width, height]])
        initial_point = np.float32([point1,point2,point3,point4])
        print(initial_point)
        print(offset_point)
        M = cv.getPerspectiveTransform(initial_point,offset_point)
        dst = cv.warpPerspective(img,M,(width, height))
        img = Image.fromarray(dst)
        resized_image = img.resize((960, 540))
        tk_image = ImageTk.PhotoImage(resized_image)
        image_label.configure(image=tk_image)
        image_label.image= tk_image
        image_label.grid(padx=20, pady=20) 

def affline_set(event):
    if (file_path is not None):
        img = cv.imread(file_path)
        height,width,ch = img.shape
        initial_point = []
        offset_point= []
        for part in shift_transform:
            if (affine_direction.get() == part):
                if "Top" in part:
                    if "Left" in part: # [x , y] x = width , y = height
                        initial_point = [[50, 50], [50, height-50], [width-50, 50]]
                        offset_point = [[initial_point[0][0]+100, initial_point[0][1]+100], initial_point[1], initial_point[2]]
                    if "Right" in part:
                        initial_point = [[width-50, 50], [width-50, height-50], [50, 50]]
                        offset_point = [[initial_point[0][0]-100, initial_point[0][1]+100], initial_point[1], initial_point[2]]
                if "Bottom" in part:
                    if "Left" in part:
                        initial_point = [[50, height-50], [50, 50], [width-50, height-50]]
                        offset_point = [[initial_point[0][0]+100, initial_point[0][1]-100], initial_point[1], initial_point[2]]
                    if "Right" in part:
                        initial_point = [[width-50, height-50], [width-50, 50], [50, height-50]]
                        offset_point = [[initial_point[0][0]-100, initial_point[0][1]-100], initial_point[1], initial_point[2]]
        affine1_var.set(str(initial_point))
        affine2_var.set(str(offset_point))
        current_obj = np.array(affine_object[affine_direction.get()])
        pts1 = np.float32(initial_point)
        pts2 = np.float32(offset_point)
         
        M = cv.getAffineTransform(pts1,pts2)
         
        dst = cv.warpAffine(img,M,(width,height))
        for tial in initial_point:
            cv.circle(dst,tial,10,[255, 255, 255],-1)
        for tial in offset_point:
            cv.circle(dst,tial,10,[255, 255, 255],-1)
        # img = Image.fromarray(dst)
        # resized_image = img.resize((960, 540))
        # tk_image = ImageTk.PhotoImage(resized_image)
        # image_label.configure(image=tk_image)
        # image_label.image= tk_image
        # image_label.grid(padx=20, pady=20) 
        plt.subplot(121),plt.imshow(img),plt.title('Input')
        plt.subplot(122),plt.imshow(dst),plt.title('Output')
        plt.show()
    return

def get_image():
    global original_image
    global file_path
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

affine_object = {
"Left Top": [[50,50],[200,50],[50,200],[10,100],[200,50],[100,250]],
"Right Top": [[50,50],[200,50],[50,200],[100,10],[250,100],[50,200]],
"Left Bottom": [[50,50],[200,50],[50,200],[100,10],[250,100],[50,200]],
"Right Bottom": [[50,50],[200,50],[50,200],[100,10],[250,100],[50,200]],
}

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
"Left Top",
"Right Top",
"Left Bottom",
"Right Bottom",
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
affine1_var = tk.StringVar()
affine2_var = tk.StringVar()
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
tk.Label(image_tab, text="Manual Deformation Affline", anchor="w", justify="left", padx=5).grid(row=13, column=0, columnspan=4, sticky="ew")
affine_transform = ttk.Combobox(image_tab, textvariable=affine_direction, values=shift_transform)
affine_transform.grid(row=14, column=0, sticky="ew")
affline_pt1 = tk.Entry(image_tab, text="", font=("Arial", 8, "bold"), textvariable=affine1_var, relief="sunken", bg="white").grid(row=14, column=1, sticky="w")
affline_pt2 = tk.Entry(image_tab, text="", font=("Arial", 8, "bold"), textvariable=affine2_var, relief="sunken", bg="white").grid(row=14, column=2, sticky="w")
tk.Label(image_tab, text="Manual Perspective Transformation", anchor="w", justify="left", padx=5).grid(row=15, column=0, columnspan=4, sticky="ew")
quadrant_i = tk.Scale(image_tab, from_=0, to=100, orient='horizontal', command=quadrant_move, length= 100, label="quadrant_i")
quadrant_ii = tk.Scale(image_tab, from_=0, to=100, orient='horizontal', command=quadrant_move, length= 100, label="quadrant ii")
quadrant_iii = tk.Scale(image_tab, from_=0, to=100, orient='horizontal', command=quadrant_move, length= 100, label="quadrant iii")
quadrant_vi = tk.Scale(image_tab, from_=0, to=100, orient='horizontal', command=quadrant_move, length= 100, label="quadrant vi")
quadrant_output = tk.Entry(image_tab, text="", font=("Arial", 8, "bold"), relief="sunken", bg="white").grid(row=17, column=0, columnspan=4, sticky="ew")
quadrant_i.grid(row=16, column=0, sticky="w")
quadrant_ii.grid(row=16, column=0, sticky="e")
quadrant_iii.grid(row=16, column=1, sticky="ew")
quadrant_vi.grid(row=16, column=2, sticky="ew")
quadrant_ii.set(100)
quadrant_vi.set(100)
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
affine_transform.bind("<<ComboboxSelected>>", affline_set)

root.mainloop()
