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
original_image = None
file_path = None
id_rec= None
x_start = None
start_rec = None
go = None
current_dir = os.path.dirname(__file__)
points = {}
for_selected = {}
selected_point = None
point_names = ["TL", "TR", "BR", "BL"]
start_pos = [(200,300), (960,300), (960,640), (200,640)]
RESIZE_RULES = {
    "TL": ("BL", "TR"),  # TL moves, BL must follow its X, TR must follow its Y
    "TR": ("BR", "TL"),  # TR moves, BR must follow its X, TL must follow its Y
    "BR": ("TR", "BL"),  # BR moves, TR must follow its X, BL must follow its Y
    "BL": ("TL", "BR")   # BL moves, TL must follow its X, BR must follow its Y
}

def on_radio_change():
    if option_var.get() == "Crop":
        # Call crop function
        pass
    elif option_var.get() == "Deform":
        # Call deform function
        pass
    elif option_var.get() == "Resize":
        # Call resize function
        pass
    elif option_var.get() == "Rotate":
        # Call rotate function
        pass

def update_line():
    # Gather coordinates of all points in order
    line_coords = []
    # We sort by the IDs or use a specific order list
    for item_id in sorted(points.keys()): 
        coords = image_canvas.coords(item_id)
        # Get center of the oval
        cx, cy = (coords[0] + coords[2])/2, (coords[1] + coords[3])/2
        line_coords.extend([cx, cy])
    
    # Update the connecting line
    image_canvas.coords(poly_id, *line_coords)

def crop_prepare():
    global transform
    transform = "crop"

def on_click(event):
    if (file_path is not None):
        global selected_point, selected_name
        items = image_canvas.find_overlapping(event.x-5, event.y-5, event.x+5, event.y+5)
        for item in items:
            if item in points:
                selected_point = item
                selected_name = points[item]
                return

def click_drag(event):
    if (file_path is not None):
        global selected_point, selected_name
        if selected_point and selected_name:
            x, y = event.x, event.y
            image_canvas.coords(selected_point, event.x-8, event.y-8, event.x+8, event.y+8)
            if (option_var.get() == "Crop"):
                x_neighbor, y_neighbor = RESIZE_RULES[selected_name]
                xn_c = image_canvas.coords(for_selected[x_neighbor])
                image_canvas.coords(for_selected[x_neighbor], x-4, xn_c[1], x+4, xn_c[3])
                yn_c = image_canvas.coords(for_selected[y_neighbor])
                image_canvas.coords(for_selected[y_neighbor], yn_c[0], y-4, yn_c[2], y+4)
            update_line()
            return

def on_release(event):
    if (file_path is not None):
        global selected_point
        if selected_point:
            image_canvas.coords(selected_point, event.x-4, event.y-4, event.x+4, event.y+4)
            selected_point = None

def on_tab_change(event):
    if (file_path is not None):
        print(event.widget.tab('current')['text'])

def get_image():
    global image_array
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
        image_array = cv.imread(file_path)
        file_name = os.path.basename(file_path)
        original_image = Image.open(file_path)
        x, y = original_image.size
        width.set(x)
        height.set(y)
        img_type = original_image.format
        bit_depth = original_image.mode
        if (width.get() > 960 and height.get() > 540):
            img_offsetx.set(width.get()/960)
            img_offsety.set(height.get()/540)
            resized_image = original_image.resize((960, 540))
        elif (width.get() < 960 and height.get() < 540):
            img_offsetx.set(1)
            img_offsety.set(1)
            resized_image = original_image
        else:
            print("Image is too big width = {width} and hieght = {hieght} which should be below 960, 940")
        reheight, rewidth = resized_image.size
        global user_image
        user_image = ImageTk.PhotoImage(resized_image)
        user_layer_id = image_canvas.create_image(100, 200, image=user_image, anchor="nw")
        image_canvas.image = user_image
        image_canvas.grid()
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
        image_canvas.tag_raise(active_layer_id, user_layer_id)
        for name, (x, y) in zip(point_names, start_pos):
            item_id = image_canvas.create_rectangle(x-4, y-4, x+4, y+4, fill="", outline="white", width=3)
            points[item_id] = name
            for_selected[name] = item_id
        flat_coords = [val for pair in start_pos for val in pair]
        global poly_id
        poly_id = image_canvas.create_polygon(*flat_coords, fill="", outline="white", dash=(4,4), width=1)
        image_canvas.bind("<Button-1>", on_click)
        image_canvas.bind("<Motion>", click_drag)
        image_canvas.bind("<ButtonRelease-1>", on_release)

contour_retrieval_modes = [
"RETR_LIST",
"RETR_TREE",
"RETR_CCOMP",
"RETR_FLOODFILL",
"RETR_EXTERNAL"
]

width = IntVar(root)
height = IntVar(root)
img_offsetx = IntVar(root)
img_offsety = IntVar(root)
option_var = tk.StringVar(value="Crop")

canvas = tk.Canvas(root, width=1780, height=990, bg="white")
main_frame = tk.Frame(canvas, width=500, height=500, bg="lightblue", bd=2, relief="sunken")
info_frame = tk.Frame(canvas, width=500, height=500, bg="lightblue", bd=2, relief="sunken")
image_frame = tk.Frame(canvas, width=1300, height=1000, bg="lightblue", bd=2, relief="solid")
canvas.grid()
main_frame.columnconfigure(0, weight=1)
main_frame.rowconfigure(0, weight=1)

contour_mode = tk.StringVar()
contour_mode.set(contour_retrieval_modes[0])

tabControl = ttk.Notebook(main_frame, width=500, height=500)
image_tab = ttk.Frame(tabControl)
operation_tab = ttk.Frame(tabControl)
advanced_tab = ttk.Frame(tabControl)
tabControl.add(image_tab, text='Image Details')
tabControl.add(operation_tab, text='Basic Operation')
tabControl.add(advanced_tab, text='Advanced Operation')
tabControl.grid(row=0, column=0,  sticky="nsew")
tabControl.bind("<<NotebookTabChanged>>", on_tab_change)
button_options = tk.Frame(image_tab, width=100)
button_options.grid(row=6, column=0, sticky='w')
url_path = tk.Entry(image_tab, text="", font=("Arial", 8, "bold"), width=75, relief="sunken", bg="white")
url_path.grid(row=0, column=0, columnspan=3, sticky="ew")
tk.Button(image_tab, text="...", command=get_image, width=5).grid(row=0, column=4, sticky="ew")
info_title = tk.Label(image_tab, text="title: ", font=("Arial", 16), anchor="w", justify="left", padx=5)
info_resize = tk.Label(image_tab, text="resize: ", font=("Arial", 16), anchor="w", justify="left", padx=5)
info_size = tk.Label(image_tab, text="original: ", font=("Arial", 16), anchor="w", justify="left", padx=5)
info_bit = tk.Label(image_tab, text="bit: ", font=("Arial", 16), anchor="w", justify="left", padx=5)
info_type = tk.Label(image_tab, text="file type: ", font=("Arial", 16), anchor="w", justify="left", padx=5)
options = ["Crop", "Deform", "Resize", "Rotate"]
for i, option in enumerate(options):
    tk.Radiobutton(
        button_options, 
        text=option, 
        variable=option_var, 
        value=option, 
        command=on_radio_change,
        indicatoron=0,
        selectcolor="lightblue",
        width=15, 
    ).grid(row=6, column=i, sticky="w")
info_title.grid(row=1, column=0, columnspan=2, sticky="ew")
info_resize.grid(row=2, column=0, columnspan=2, sticky="ew")
info_size.grid(row=3, column=0, columnspan=2, sticky="ew")
info_bit.grid(row=4, column=0, columnspan=2, sticky="ew")
info_type.grid(row=5, column=0, columnspan=2, sticky="ew")

combo = ttk.Combobox(operation_tab, textvariable=contour_mode, values=contour_retrieval_modes)
minimum = tk.Scale(operation_tab, from_=0, to_=255, orient='horizontal', length= 200, label="minimum")
maximum = tk.Scale(operation_tab, from_=0, to=255, orient='horizontal', length= 200, label="maximum")
entry = tk.Scale(operation_tab, from_=0, to=12, orient='horizontal', length= 48, label="defects")
combo.grid(row=0, column=0, columnspan=2, sticky="ew", pady=10)
minimum.grid(row=1, column=0, columnspan=2, sticky="nsew")
maximum.grid(row=2, column=0, columnspan=2, sticky="nsew")
entry.grid(row=3, column=0, columnspan=2, sticky="nsew")

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
        image_canvas.create_line(40, y, 1240, y, fill="lightgray")
user_layer = Image.new("RGBA", (960, 540), (0, 0, 0, 0))
global active_layer
active_layer = ImageTk.PhotoImage(user_layer)
active_layer_id = image_canvas.create_image(100, 200, image=active_layer, anchor="nw")
image_canvas.image = active_layer
image_canvas.grid()
image_canvas.config(cursor="tcross")

for i in range(4):
    root.grid_columnconfigure(i, weight=1)
root.mainloop()
