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
