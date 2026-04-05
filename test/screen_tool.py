import tkinter as tk

start_x = start_y = end_x = end_y = 0

def on_mouse_down(event):
    global start_x, start_y
    start_x, start_y = event.x, event.y

def on_mouse_drag(event):
    canvas.coords(rect, start_x, start_y, event.x, event.y)

def on_mouse_up(event):
    global end_x, end_y
    end_x, end_y = event.x, event.y

    print(f"Start: ({start_x}, {start_y})")
    print(f"End: ({end_x}, {end_y})")

    width = abs(end_x - start_x)
    height = abs(end_y - start_y)

    print(f"Size: {width}x{height}")

root = tk.Tk()
root.attributes("-fullscreen", True)

canvas = tk.Canvas(root, cursor="cross")
canvas.pack(fill="both", expand=True)

rect = canvas.create_rectangle(0, 0, 0, 0, outline="red")

canvas.bind("<ButtonPress-1>", on_mouse_down)
canvas.bind("<B1-Motion>", on_mouse_drag)
canvas.bind("<ButtonRelease-1>", on_mouse_up)

root.mainloop()