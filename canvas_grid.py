import math
import numpy as np
import os
from matplotlib import pyplot as plt
import cv2 as cv
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
Auto_Map = {}
for_selected = {}
line_segment = {}
rot_obj = {}
selected_point = None
point_names = ["TL", "TR", "BR", "BL"]
start_pos = [(200,300), (960,300), (960,640), (200,640)]
RESIZE_RULES = {
    "TL": ("BL", "TR"),  # TL moves, BL must follow its X, TR must follow its Y
    "TR": ("BR", "TL"),  # TR moves, BR must follow its X, TL must follow its Y
    "BR": ("TR", "BL"),  # BR moves, TR must follow its X, BL must follow its Y
    "BL": ("TL", "BR")   # BL moves, TL must follow its X, BR must follow its Y
}

def save_set():
    global image_array
    y, x, ch = img_bgr.shape
    print(f"{x} : {y}\n{width.get()} : {height.get()}")
    im = cv.cvtColor(img_bgr, cv.COLOR_BGR2RGB)
    width.set(x)
    height.set(y)
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
    image_array = im

def reset_apply():
    im = cv.cvtColor(image_array, cv.COLOR_BGR2RGB)
    img = Image.fromarray(im)
    resized_image = img.resize((960, 540))
    tk_image = ImageTk.PhotoImage(resized_image)
    image_canvas.itemconfig(user_layer_id, image=tk_image)
    image_canvas.tk_image = tk_image 
    image_canvas.tag_raise(active_layer_id, user_layer_id)

def affline_set(x, y):
    if (file_path is not None):
        global image_array
        global img_offsetx
        global img_offsety
        x_offset = img_offsetx.get()
        y_offset = img_offsety.get()
        IMG_ORIGIN_X = 100
        IMG_ORIGIN_Y = 200
        height,width,ch = image_array.shape
        targets = [0, width, height]
        initial_point = []
        offset_point = []
        if (option_var.get() != "Rotate") :
            for i, item_id in enumerate(sorted(points.keys())):
                if (points[item_id] in RESIZE_RULES[selected_name] or points[item_id] is selected_name and option_var.get() == "Deform" or option_var.get() == "Crop" or option_var == "Resize"):
                    print(f"{i} : {item_id} : {selected_name} : {selected_point}")
                    a, b, c, d = image_canvas.coords(item_id)
                    # 1. Find the center of the UI square on the canvas
                    canvas_x = (a + c) / 2
                    canvas_y = (b + d) / 2
                    orig_anchor_x, orig_anchor_y = start_pos[i]
                    # 2. Subtract the 100/200 offset to get 'Image Space'
                    # 3. Add the +4 inner offset
                    local_x = (canvas_x - IMG_ORIGIN_X) + 4
                    local_y = (canvas_y - IMG_ORIGIN_Y) + 4
                    # 4. Scale to original image size and cast for OpenCV
                    # Note: ensure x_offset is (Original_Width / Canvas_Width)
                    scaled_x = (local_x * x_offset)
                    scaled_y = (local_y * y_offset)
                    initial_point.append([scaled_x, scaled_y])
                    if (option_var.get() == "Resize" and points[item_id] == "TL"):
                        off_setx, off_sety =  scaled_x, scaled_y
                    if (option_var.get() == "Resize" and points[item_id] == "BR"):
                        resize_width, resize_height = scaled_x - off_setx, scaled_y - off_sety
                    point1 = min(targets, key=lambda x: abs(x - scaled_x))
                    point2 = min(targets, key=lambda x: abs(x - scaled_y))
                    offset_point.append([point1, point2])
            pts1 = np.float32(offset_point)
            pts2 = np.float32(initial_point)
            print(f"{pts1} : {pts2}")
        if (option_var.get() == "Rotate"):
            for v in rot_obj:
                a, b, c, d = image_canvas.coords(rot_obj[v])
                canvas_x = (a + c) / 2
                canvas_y = (b + d) / 2
                orig_anchor_x, orig_anchor_y = width/2, height/2
                local_x = (canvas_x - IMG_ORIGIN_X) + 4
                local_y = (canvas_y - IMG_ORIGIN_Y) + 4
                scaled_x = (local_x * x_offset)
                scaled_y = (local_y * y_offset)
                if (v == 0):
                    theta_y, theta_x = scaled_y, scaled_x
                else:
                    center_x, center_y = scaled_x, scaled_y
            dy = center_y - theta_y
            dx = theta_x - center_x
            radians = math.atan2(dy, dx)
            degrees = math.degrees(radians) - 90

            # Optional: Normalize to 0-360 range if you don't want negative degrees
            if degrees < 0:
                degrees += 360
            print(f"{dx} : {dy}\n{center_x} : {center_y}\n{radians} : {degrees}")
        global dst
        if (option_var.get() == "Deform" or option_var.get() == "Rotate"):
            if (option_var.get() == "Deform"):
                M = cv.getAffineTransform(pts1,pts2)
            else:
                M = cv.getRotationMatrix2D(((width-1)/2.0,(height-1)/2.0),degrees,1)
            dst = cv.warpAffine(image_array,M,(width,height))
        elif (option_var.get() == "Crop"):
            M = cv.getPerspectiveTransform(pts2,pts1)
            dst = cv.warpPerspective(image_array,M,(width,height))
        elif (option_var.get() == "Resize"):
            dst = cv.resize(image_array,(int(resize_width), int(resize_height)), interpolation = cv.INTER_CUBIC)
        global img_bgr
        img_bgr = cv.cvtColor(dst, cv.COLOR_BGR2RGB)
        img = Image.fromarray(img_bgr)
        resized_image = img.resize((960, 540))
        tk_image = ImageTk.PhotoImage(resized_image)
        image_canvas.itemconfig(user_layer_id, image=tk_image)
        image_canvas.tk_image = tk_image 
        image_canvas.tag_raise(active_layer_id, user_layer_id)

def on_radio_change():
    for i, name in enumerate(point_names):
        if (option_var.get() != "Rotate" and image_canvas.bbox(for_selected[name]) is None):
            image_canvas.itemconfigure(for_selected[name], state='normal')
            if image_canvas.bbox(rot_obj[0]) is not None:
                for rotation in rot_obj:
                    image_canvas.itemconfigure(rot_obj[rotation], state='hidden')
        elif (option_var.get() == "Rotate"):
            for rotation in rot_obj:
                if (image_canvas.bbox(rot_obj[rotation]) is None):
                    image_canvas.itemconfigure(rot_obj[rotation], state='normal')
                else:
                    break
        if option_var.get() == "Crop":
            x, y = start_pos[i]
            image_canvas.coords(for_selected[name], x-4, y-4, x+4, y+4)
            # Call resize function
            pass
        elif option_var.get() == "Deform":
            x, y = start_pos[i]
            image_canvas.coords(for_selected[name], x-4, y-4, x+4, y+4)
            # Call resize function
            pass
        elif option_var.get() == "Resize":
            x, y = Auto_Map[name]
            image_canvas.coords(for_selected[name], x-4, y-4, x+4, y+4)
            # Call resize function
            pass
        elif option_var.get() == "Rotate":
            image_canvas.itemconfigure(for_selected[name], state='hidden')
            # Call rotate function
            pass
    if option_var.get() == "Rotate":
        print("here")
        print(line_segment)
        for v, line in enumerate(line_segment):
            print(f"{line} : {rot_obj[v]} : {v} : here")
            image_canvas.coords(rot_obj[v], line[0]-4, line[1]-4, line[0]+4, line[1]+4)
    update_line()

def update_line():
    # Gather coordinates of all points in order
    line_coords = []
    # We sort by the IDs or use a specific order list
    if (option_var.get() != "Rotate"):
        for item_id in sorted(points.keys()): 
            coords = image_canvas.coords(item_id)
            # Get center of the oval
            cx, cy = (coords[0] + coords[2])/2, (coords[1] + coords[3])/2
            line_coords.extend([cx, cy])
    else:
        for v in rot_obj:
            coords = image_canvas.coords(rot_obj[v])
            # Get center of the oval
            cx, cy = coords[0]+4, coords[1]+4
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
        if (option_var.get() != "Rotate"):
            for item in items:
                if item in points:
                    selected_point = item
                    selected_name = points[item]
                    return
        else:
            for item in items:
                if item == rot_obj[0]:
                    selected_point = item
                    selected_name = rot_obj[0]
                    return

options = ["Crop", "Deform", "Resize", "Rotate"]
def click_drag(event):
    if (file_path is not None):
        global selected_point, selected_name
        if selected_point and selected_name:
            x, y = event.x, event.y
            image_canvas.coords(selected_point, event.x-8, event.y-8, event.x+8, event.y+8)
            if (option_var.get() == "Crop" or option_var.get() == "Resize"):
                x_neighbor, y_neighbor = RESIZE_RULES[selected_name]
                xn_c = image_canvas.coords(for_selected[x_neighbor])
                image_canvas.coords(for_selected[x_neighbor], x-4, xn_c[1], x+4, xn_c[3])
                yn_c = image_canvas.coords(for_selected[y_neighbor])
                image_canvas.coords(for_selected[y_neighbor], yn_c[0], y-4, yn_c[2], y+4)
            update_line()
            affline_set(x, y)
            return

def on_release(event):
    if (file_path is not None):
        global selected_point
        x, y = event.x, event.y
        if selected_point:
            image_canvas.coords(selected_point, x-4, y-4, x+4, y+4)
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
        global line_segment
        line_segment = [[reheight/2+100, 200], [reheight/2+100, rewidth/2+200]]
        global user_image
        user_image = ImageTk.PhotoImage(resized_image)
        global user_layer_id
        user_layer_id = image_canvas.create_image(100, 200, image=user_image, anchor="nw")
        image_canvas.image = user_layer_id
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
        for v, line in enumerate(line_segment):
            rotate_segment = image_canvas.create_rectangle(line[0]-4, line[1]-4, line[0]+4, line[1]+4, fill="", outline="white", width=3)
            rot_obj[v] = rotate_segment
            print(f"{rotate_segment} : {rot_obj[v]} : {v}")
            image_canvas.itemconfigure(rotate_segment, state='hidden')
        for name, (x, y) in zip(point_names, start_pos):
            item_id = image_canvas.create_rectangle(x-4, y-4, x+4, y+4, fill="", outline="white", width=3)
            if (name == "TL"):
                Auto_Map[name] = [100, 200]
            if (name == "TR"):
                Auto_Map[name] = [reheight+100, 200]
            if (name == "BR"):
                Auto_Map[name] = [reheight+100, rewidth+200]
            if (name == "BL"):
                Auto_Map[name] = [100, rewidth+200]
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
image_frame = tk.Frame(canvas, width=1300, height=1000, bg="", bd=2, relief="solid")
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
button_control = tk.Frame(image_frame, width=100, height=50, bg="", bd=2, relief="solid")
button_control.place(x=820, y=745)
reset_button = tk.Button(button_control, text="RESET", command=reset_apply, width=15).grid(row=0, column=0, sticky="ew", padx=3)
apply_button = tk.Button(button_control, text="APPLY", command=save_set, width=15).grid(row=0, column=1, sticky="ew", padx=3)
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
