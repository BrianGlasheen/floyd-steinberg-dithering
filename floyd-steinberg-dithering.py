from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog
import os 

global DIR_PATH
DIR_PATH = os.path.dirname(os.path.realpath(__file__))

root = tk.Tk()
root.wm_geometry("900x400")

canvas = tk.Canvas(root, width=400, height=400)
canvas.grid(row=0, column=1, rowspan=20)
canvas_d = tk.Canvas(root, width=400, height=400)
canvas_d.grid(row=0, column=2, rowspan=20)

upload_button = tk.Button(root, text="Upload image", command=lambda: upload_img(canvas))
upload_button.grid(row=0, column=0, sticky=tk.NSEW)

dither_button = tk.Button(root, text="Dither", command=lambda: dither(1))
dither_button.grid(row=1, column=0, sticky=tk.NSEW)

save_button = tk.Button(root, text="Save image", command=lambda: save_img())
save_button.grid(row=2, column=0, sticky=tk.NSEW)



def closest_step(pixels, steps):
    return tuple([round(steps * pixel / 255) * int(255 / steps) for pixel in pixels])

def quant_error_calc(pixels, x, y, quant_error, factor):
    result = add(pixels[x, y], multiply(quant_error, factor))
    return int(result[0]), int(result[1]), int(result[2])

def dist_err(image, pixels, x, y, error):
    add_err(image, pixels, 7 / 16.0, x + 1, y, error)
    add_err(image, pixels, 3 / 16.0, x - 1, y + 1, error)
    add_err(image, pixels, 5 / 16.0, x, y + 1, error)
    add_err(image, pixels, 1 / 16.0, x + 1, y + 1, error)

def add_err(image, pixels, factor, x, y, error):
    if x <= 0 or x >= image.size[0] or y <= 0 or y >= image.size[1]:
        return
    try:
        r, g, b, a = pixels[x, y]
    except ValueError:
        r, g, b = pixels[x, y]
    pixels[x, y] = (int(r+error[0]*factor), int(g+error[1]*factor), int(b+error[2]*factor), 255)       

def dither(steps):
    try:
        image = Image.open(root.filename)
    except AttributeError:
        print('No image')
        return
    pixels = image.load()
    for x in range(image.size[0]):
        for y in range(image.size[1]):
            old_pixel = pixels[x, y]
            new_pixel = closest_step(old_pixel, steps)

            pixels[x, y] = new_pixel

            error = tuple([old_pixel[0] - new_pixel[0], old_pixel[1] - new_pixel[1], old_pixel[2] - new_pixel[2]])

            dist_err(image, pixels, x, y, error)

    draw(image, 0)

def draw(image, i):
    global tk_img, imagesprite, imagesprite_d, tk_img_d, dithered
    if i:
        tk_img = ImageTk.PhotoImage(image) 
        imagesprite = canvas.create_image(200, 200, image=tk_img)
    else:
        tk_img_d = ImageTk.PhotoImage(image)
        imagesprite_d = canvas_d.create_image(200, 200, image=tk_img_d)
        dithered = image

def upload_img(canvas):
    root.filename = filedialog.askopenfilename(initialdir = DIR_PATH,title = "Select file",filetypes = (("JPG","*.jpg"),("PNG","*.png")))
    draw(Image.open(root.filename), 1)

def save_img():
    try:
        root.filename1 = filedialog.asksaveasfilename(initialdir = DIR_PATH,title = "Select file",filetypes = (("Png","*.png"),("All types","*.all")))
        dithered.save(root.filename1 + '.png')
    except (NameError, KeyError) as e:
        print('Error saving')

root.mainloop()