from PIL import Image
import sys
import os
from tkinter import *
from tkinter import ttk
from tkinter.colorchooser import askcolor
from tkinter.filedialog import asksaveasfile
import webbrowser


# Program version
VERSION = "1.0"


# Function to load resource when the program is compiled into an executable
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# App texts, if you want to add another language, copy and paste the english dictionary, replace the values and then
# modify the line with lang = english with the language of your choice
english = {
    "change_color": "Change Color",
    "choose_color": "Choose Color",
    "menu_file": "File",
    "menu_about": "About",
    "menu_open": "Open Current Image",
    "menu_save": "Save Current Image",
    "menu_exit": "Exit",
    "menu_license": "Open License",
    "menu_github": "GitHub Project",
    "padoru_type": "Type",
    "padoru_none": "None",
    "padoru_face": "Face",
    "padoru_mouth": "Mouth",
    "padoru_mouth_a": "Normal",
    "padoru_mouth_b": "Neutral",
    "padoru_eyes": "Eyes",
    "padoru_bag": "Bag",
    "padoru_clothes": "Clothes",
    "padoru_accessory": "Neck Accessory",
    "padoru_accessory_a": "Red Bow",
    "padoru_accessory_b": "Leaf",
    "padoru_hair": "Hair",
    "padoru_hat": "Hat",
    "background": "Background Color",
    "background_a": "Transparent",
    "background_b": "Uniform Color"
}
lang = english


# Script to set the color of a specific part
def change_img_color(path, color):
    temp = Image.open(path)
    temp = temp.convert("RGBA")
    data = temp.getdata()
     
    new_image = []
    for item in data:
        if item[3] != 0:
            new_image.append((color[0], color[1], color[2], item[3]))
        else:
            new_image.append(item)

    temp.putdata(new_image)
    return temp


# Script to combine all the images
def merge(images):
    if bg_type != 0:
        bg = Image.new('RGBA', (500, 500), color=(colors["bg"][0], colors["bg"][1], colors["bg"][2], 255))
    else:
        bg = Image.new('RGBA', (500, 500), color=(0, 0, 0, 0))
    for i in range(len(images)):
        bg.paste(images[i], (0, 0), images[i])
    return bg


# All the defaults colors of the padoru, I do not recommend editing this
colors = {
    # BG #
    "bg": (0, 255, 0),
    # FACE #
    "face_empty": (243, 225, 217),
    # MOUTH A #
    "mouth_a_c1": (208, 112, 124),
    "mouth_a_outline": (0, 0, 0),
    # MOUTH B #
    "mouth_b_outline": (0, 0, 0),
    # EYES A #
    "eyes_a_c1": (75, 66, 123),
    "eyes_a_c2": (170, 156, 198),
    "eyes_a_outline": (0, 0, 0),
    # EYES B #
    "eyes_b_c1": (65, 60, 71),
    "eyes_b_c2": (182, 196, 109),
    "eyes_b_outline": (0, 0, 0),
    # EYES C #
    "eyes_c_c1": (56, 88, 84),
    "eyes_c_c2": (106, 158, 156),
    "eyes_c_outline": (0, 0, 0),
    # BAG #
    "bag_c1": (252, 250, 251),
    "bag_c2": (217, 213, 209),
    "bag_outline": (0, 0, 0),
    # BODY #
    "body_c1": (234, 221, 225),
    "body_c2": (198, 50, 53),
    "body_c3": (141, 21, 30),
    "body_outline": (0, 0, 0),
    # NECK A #
    "neck_a_c1": (198, 50, 53),
    "neck_a_outline": (0, 0, 0),
    # NECK B #
    "neck_b_c1": (47, 133, 77),
    "neck_b_outline": (0, 0, 0),
    # HAIR A #
    "hair_a_c1": (161, 118, 77),
    "hair_a_c2": (233, 200, 139),
    "hair_a_c3": (235, 227, 195),
    "hair_a_c4": (173, 8, 54),
    "hair_a_outline": (0, 0, 0),
    # HAIR B #
    "hair_b_c1": (52, 44, 70),
    "hair_b_c2": (82, 68, 110),
    "hair_b_c3": (121, 107, 155),
    "hair_b_outline": (0, 0, 0),
    # HAIR C #
    "hair_c_c1": (163, 100, 103),
    "hair_c_c2": (221, 187, 181),
    "hair_c_c3": (243, 212, 204),
    "hair_c_outline": (0, 0, 0),
    # HAT #
    "hat_c1": (234, 221, 225),
    "hat_c2": (158, 125, 132),
    "hat_c3": (198, 50, 53),
    "hat_c4": (129, 25, 33),
    "hat_outline": (0, 0, 0)
}

# Don't ask why this exists
letters = ["a", "b", "c"]


# Default values, those are not linked to the buttons and combo boxes
neck_type = 0
mouth_type = 1
eyes_type = 1
hair_type = 1
bg_type = 0


# Script to create the image, note that the order of each line is the order of rendering.
# This is script is slow though, I don't know if it's when it changes the color of the images or when it merge them
# together, but it's either this script, or change_img_color() or merge() that need to be optimised. If you know
# PIL better than me, feel free to optimise it and make a PR on GitHub
def gen():
    parts_list = []

    # FACE #
    parts_list.append(change_img_color(resource_path("parts/face/face_empty.png"), colors["face_empty"]))
    # MOUTH #
    if mouth_type == 1:
        parts_list.append(change_img_color(resource_path("parts/mouth_a/mouth_a_c1.png"), colors["mouth_a_c1"]))
        parts_list.append(change_img_color(resource_path("parts/mouth_a/mouth_a_outline.png"), colors["mouth_a_outline"]))
    elif mouth_type == 2:
        parts_list.append(change_img_color(resource_path("parts/mouth_b/mouth_b_outline.png"), colors["mouth_b_outline"]))
    # EYES #
    parts_list.append(change_img_color(resource_path("parts/eyes_" + letters[eyes_type - 1] + "/eyes_" + letters[eyes_type - 1] + "_c1.png"), colors["eyes_" + letters[eyes_type - 1] + "_c1"]))
    parts_list.append(change_img_color(resource_path("parts/eyes_" + letters[eyes_type - 1] + "/eyes_" + letters[eyes_type - 1] + "_c2.png"), colors["eyes_" + letters[eyes_type - 1] + "_c2"]))
    parts_list.append(change_img_color(resource_path("parts/eyes_" + letters[eyes_type - 1] + "/eyes_" + letters[eyes_type - 1] + "_outline.png"), colors["eyes_" + letters[eyes_type - 1] + "_outline"]))
    # BAG #
    parts_list.append(change_img_color(resource_path("parts/bag/bag_c1.png"), colors["bag_c1"]))
    parts_list.append(change_img_color(resource_path("parts/bag/bag_c2.png"), colors["bag_c2"]))
    parts_list.append(change_img_color(resource_path("parts/bag/bag_outline.png"), colors["bag_outline"]))
    # BODY #
    parts_list.append(change_img_color(resource_path("parts/body/body_c1.png"), colors["body_c1"]))
    parts_list.append(change_img_color(resource_path("parts/body/body_c2.png"), colors["body_c2"]))
    parts_list.append(change_img_color(resource_path("parts/body/body_c3.png"), colors["body_c3"]))
    parts_list.append(change_img_color(resource_path("parts/body/body_outline.png"), colors["body_outline"]))
    # NECK #
    if not neck_type == 0:
        parts_list.append(change_img_color(resource_path("parts/neck_" + letters[neck_type - 1] + "/neck_" + letters[neck_type - 1] + "_c1.png"), colors["neck_" + letters[neck_type - 1] + "_c1"]))
        parts_list.append(change_img_color(resource_path("parts/neck_" + letters[neck_type - 1] + "/neck_" + letters[neck_type - 1] + "_outline.png"), colors["neck_" + letters[neck_type - 1] + "_outline"]))
    # HAIR #
    parts_list.append(change_img_color(resource_path("parts/hair_" + letters[hair_type - 1] + "/hair_" + letters[hair_type - 1] + "_c1.png"), colors["hair_" + letters[hair_type - 1] + "_c1"]))
    parts_list.append(change_img_color(resource_path("parts/hair_" + letters[hair_type - 1] + "/hair_" + letters[hair_type - 1] + "_c2.png"), colors["hair_" + letters[hair_type - 1] + "_c2"]))
    parts_list.append(change_img_color(resource_path("parts/hair_" + letters[hair_type - 1] + "/hair_" + letters[hair_type - 1] + "_c3.png"), colors["hair_" + letters[hair_type - 1] + "_c3"]))
    if hair_type == 1:
        parts_list.append(change_img_color(resource_path("parts/hair_a/hair_a_c4.png"), colors["hair_a_c4"]))
    parts_list.append(change_img_color(resource_path("parts/hair_" + letters[hair_type - 1] + "/hair_" + letters[hair_type - 1] + "_outline.png"), colors["hair_" + letters[hair_type - 1] + "_outline"]))
    # HAT #
    parts_list.append(change_img_color(resource_path("parts/hat/hat_c1.png"), colors["hat_c1"]))
    parts_list.append(change_img_color(resource_path("parts/hat/hat_c2.png"), colors["hat_c2"]))
    parts_list.append(change_img_color(resource_path("parts/hat/hat_c3.png"), colors["hat_c3"]))
    parts_list.append(change_img_color(resource_path("parts/hat/hat_c4.png"), colors["hat_c4"]))
    parts_list.append(change_img_color(resource_path("parts/hat/hat_outline.png"), colors["hat_outline"]))

    output = merge(parts_list)
    return output


# For some reason importing this at the beginning don't work
from PIL import Image, ImageTk

final = gen()

# Setup the program
root = Tk()
root.geometry("1000x500")
root.title("Infinite Padoru | V" + VERSION + " | By @Escartem")
root.iconbitmap(resource_path("icon.ico"))
root.resizable(False, False)


def open_img():
    gen().show()


def save_img():
    temp = gen()
    files = [('PADORU', '*.png')]
    f = asksaveasfile(mode='w', filetypes=files)
    if f is None:
        return
    f.close()
    temp.save(f.name)


def update_canvas():
    temp = ImageTk.PhotoImage(gen())
    canvas.itemconfig(image_sprite, image=temp)
    canvas.image = temp


def quit():
    exit()


# Create the menu bar
menu_bar = Menu(root)

file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label=lang["menu_open"], accelerator="CTRL+O", command=open_img)
file_menu.add_command(label=lang["menu_save"], accelerator="CTRL+S", command=save_img)
file_menu.add_separator()
file_menu.add_command(label=lang["menu_exit"], accelerator="CTRL+Q", command=quit)
root.bind_all("<Control-o>", lambda x: open_img())
root.bind_all("<Control-s>", lambda x: save_img())
root.bind_all("<Control-q>", lambda x: quit())

about_menu = Menu(menu_bar, tearoff=0)
about_menu.add_command(label=lang["menu_license"], command=lambda: webbrowser.open("https://github.com/Escartem/InfinitePadorus/blob/main/LICENSE"))
about_menu.add_command(label=lang["menu_github"], command=lambda: webbrowser.open("https://github.com/Escartem/InfinitePadorus"))

menu_bar.add_cascade(label=lang["menu_file"], menu=file_menu)
menu_bar.add_cascade(label=lang["menu_about"], menu=about_menu)

root.config(menu=menu_bar)

# Create the main frames, one for the buttons, one for the rendered image
options_frame = Frame(root, background="#FFF0C1", bd=1, relief="groove")
canvas_frame = Frame(root, background="#D2E2FB", bd=1, relief="groove")

options_frame.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
canvas_frame.grid(row=0, column=1, sticky="nsew", padx=2, pady=2)

root.grid_columnconfigure(0, weight=0)
root.grid_columnconfigure(1, weight=2)
root.grid_rowconfigure(0, weight=3)

canvas = Canvas(canvas_frame, width=512, height=512)
canvas.place(relx=0.5, rely=0.5, anchor=CENTER)

img = ImageTk.PhotoImage(gen())

image_sprite = canvas.create_image(256, 256, image=img)


# Everything after this part is just setting up the buttons, I tried to make some sort of universal change_color()
# function but it didn't worked, so everything is a little bit copied pasted, if you know tkinter feel free to change
# this and make a PR

# FACE
def update_face_color():
    elem = "face_empty"
    color = askcolor(title=lang["choose_color"], color=colors[elem])
    colors[elem] = (abs(round(color[0][0]-5)), round(abs(color[0][1]-5)), round(abs(color[0][2])-1))
    face_btn["bg"] = color[1]
    update_canvas()


face_frame = LabelFrame(options_frame, text=lang["padoru_face"], bd=2, background="#FFF0C1", relief="groove")
face_frame.grid(row=0, column=0, padx=5, pady=5)

face_btn = Button(face_frame, text=lang["change_color"], command=update_face_color, bg='#%02x%02x%02x' % colors["face_empty"])
face_btn.grid(column=0, row=1, padx=5, pady=5)


# MOUTH
def mouth_update(event):
    global mouth_type
    ind = mouth_values.index(event.widget.get())
    mouth_type = ind+1
    if ind == 0:
        mouth_btn["state"] = "normal"
        mouth_btn["bg"] = '#%02x%02x%02x' % colors["mouth_a_c1"]
    else:
        mouth_btn["state"] = "disabled"
        mouth_btn["bg"] = "#d4d4d4"
    update_canvas()


def update_mouth_color():
    elem = "mouth_a_c1"
    color = askcolor(title=lang["choose_color"], color=colors[elem])
    colors[elem] = (round(abs(color[0][0]-5)), round(abs(color[0][1]-5)), round(abs(color[0][2])-1))
    mouth_btn["bg"] = color[1]
    update_canvas()


mouth_frame = LabelFrame(options_frame, text=lang["padoru_mouth"], bd=2, background="#FFF0C1", relief="groove")
mouth_frame.grid(row=0, column=1, padx=5, pady=5)

mouth_values = [lang["padoru_mouth_a"], lang["padoru_mouth_b"]]
mouth_combo = ttk.Combobox(mouth_frame, values=mouth_values, state="readonly")
mouth_combo.grid(column=0, row=0, padx=5, pady=5)
mouth_combo.current(0)
mouth_combo.bind("<<ComboboxSelected>>", mouth_update)
mouth_btn = Button(mouth_frame, text=lang["change_color"], command=update_mouth_color, bg='#%02x%02x%02x' % colors["mouth_a_c1"])
mouth_btn.grid(column=0, row=1, padx=5, pady=5)


# EYES
def eyes_update(event):
    global eyes_type
    ind = eyes_values.index(event.widget.get())
    eyes_type = ind+1
    eyes_btn_c1["bg"] = '#%02x%02x%02x' % colors["eyes_" + letters[eyes_type - 1] + "_c1"]
    eyes_btn_c2["bg"] = '#%02x%02x%02x' % colors["eyes_" + letters[eyes_type - 1] + "_c2"]
    update_canvas()


def update_eyes_color(cl):
    elem = "eyes_" + letters[eyes_type - 1] + "_" + cl
    color = askcolor(title=lang["choose_color"], color=colors[elem])
    colors[elem] = (abs(round(color[0][0]-5)), round(abs(color[0][1]-5)), round(abs(color[0][2])-1))
    if cl == "c1":
        eyes_btn_c1["bg"] = color[1]
    elif cl == "c2":
        eyes_btn_c2["bg"] = color[1]
    update_canvas()


eyes_frame = LabelFrame(options_frame, text=lang["padoru_eyes"], bd=2, background="#FFF0C1", relief="groove")
eyes_frame.grid(row=0, column=3, padx=5, pady=5)

eyes_values = [lang["padoru_type"] + " A", lang["padoru_type"] + " B", lang["padoru_type"] + " C"]
eyes_combo = ttk.Combobox(eyes_frame, values=eyes_values, state="readonly")
eyes_combo.grid(column=0, row=0, padx=5, pady=5)
eyes_combo.current(0)
eyes_combo.bind("<<ComboboxSelected>>", eyes_update)

eyes_btn_c1 = Button(eyes_frame, text=lang["change_color"], command=lambda: update_eyes_color("c1"), bg='#%02x%02x%02x' % colors["eyes_a_c1"])
eyes_btn_c1.grid(column=0, row=1, padx=5, pady=5)

eyes_btn_c2 = Button(eyes_frame, text=lang["change_color"], command=lambda: update_eyes_color("c2"), bg='#%02x%02x%02x' % colors["eyes_a_c2"])
eyes_btn_c2.grid(column=0, row=2, padx=5, pady=5)


# BAG
def update_bag_color(cl):
    elem = "bag_" + cl
    color = askcolor(title=lang["choose_color"], color=colors[elem])
    colors[elem] = (abs(round(color[0][0]-5)), round(abs(color[0][1]-5)), round(abs(color[0][2])-1))
    if cl == "c1":
        bag_btn_c1["bg"] = color[1]
    elif cl == "c2":
        bag_btn_c2["bg"] = color[1]
    update_canvas()


bag_frame = LabelFrame(options_frame, text=lang["padoru_bag"], bd=2, background="#FFF0C1", relief="groove")
bag_frame.grid(row=1, column=0, padx=5, pady=5)

bag_btn_c1 = Button(bag_frame, text=lang["change_color"], command=lambda: update_bag_color("c1"), bg='#%02x%02x%02x' % colors["bag_c1"])
bag_btn_c1.grid(column=0, row=1, padx=5, pady=5)

bag_btn_c2 = Button(bag_frame, text=lang["change_color"], command=lambda: update_bag_color("c2"), bg='#%02x%02x%02x' % colors["bag_c2"])
bag_btn_c2.grid(column=0, row=2, padx=5, pady=5)


# BODY
def update_body_color(cl):
    elem = "body_" + cl
    color = askcolor(title=lang["choose_color"], color=colors[elem])
    colors[elem] = (abs(round(color[0][0]-5)), round(abs(color[0][1]-5)), round(abs(color[0][2])-1))
    if cl == "c1":
        body_btn_c1["bg"] = color[1]
    elif cl == "c2":
        body_btn_c2["bg"] = color[1]
    elif cl == "c3":
        body_btn_c3["bg"] = color[1]
    update_canvas()


body_frame = LabelFrame(options_frame, text=lang["padoru_clothes"], bd=2, background="#FFF0C1", relief="groove")
body_frame.grid(row=1, column=1, padx=5, pady=5)

body_btn_c1 = Button(body_frame, text=lang["change_color"], command=lambda: update_body_color("c1"), bg='#%02x%02x%02x' % colors["body_c1"])
body_btn_c1.grid(column=0, row=1, padx=5, pady=5)

body_btn_c2 = Button(body_frame, text=lang["change_color"], command=lambda: update_body_color("c2"), bg='#%02x%02x%02x' % colors["body_c2"])
body_btn_c2.grid(column=0, row=2, padx=5, pady=5)

body_btn_c3 = Button(body_frame, text=lang["change_color"], command=lambda: update_body_color("c3"), bg='#%02x%02x%02x' % colors["body_c3"])
body_btn_c3.grid(column=0, row=3, padx=5, pady=5)


# NECK TYPE
def neck_update(event):
    global neck_type
    ind = neck_values.index(event.widget.get())
    neck_type = ind
    if ind == 0:
        neck_btn["state"] = "disabled"
        neck_btn["bg"] = "#d4d4d4"
    else:
        neck_btn["state"] = "normal"
        neck_btn["bg"] = '#%02x%02x%02x' % colors["neck_" + letters[neck_type - 1] + "_c1"]
    update_canvas()


def update_neck_color():
    elem = "neck_" + letters[neck_type - 1] + "_c1"
    color = askcolor(title=lang["choose_color"], color=colors[elem])
    colors[elem] = (round(abs(color[0][0]-5)), round(abs(color[0][1]-5)), round(abs(color[0][2])-1))
    neck_btn["bg"] = color[1]
    update_canvas()


neck_frame = LabelFrame(options_frame, text=lang["padoru_accessory"], bd=2, background="#FFF0C1", relief="groove")
neck_frame.grid(row=1, column=3, padx=5, pady=5)

neck_values = [lang["padoru_none"], lang["padoru_accessory_a"], lang["padoru_accessory_b"]]
neck_combo = ttk.Combobox(neck_frame, values=neck_values, state="readonly")
neck_combo.grid(column=0, row=0, padx=5, pady=5)
neck_combo.current(0)
neck_combo.bind("<<ComboboxSelected>>", neck_update)
neck_btn = Button(neck_frame, text=lang["change_color"], command=update_neck_color, state="disabled", bg="#d4d4d4")
neck_btn.grid(column=0, row=1, padx=5, pady=5)


# HAIR
def hair_update(event):
    global hair_type
    ind = hair_values.index(event.widget.get())
    hair_type = ind+1
    hair_btn_c1["bg"] = '#%02x%02x%02x' % colors["hair_" + letters[hair_type - 1] + "_c1"]
    hair_btn_c2["bg"] = '#%02x%02x%02x' % colors["hair_" + letters[hair_type - 1] + "_c2"]
    hair_btn_c3["bg"] = '#%02x%02x%02x' % colors["hair_" + letters[hair_type - 1] + "_c3"]
    if ind == 0:
        hair_btn_c4["state"] = "normal"
        hair_btn_c4["bg"] = '#%02x%02x%02x' % colors["hair_a_c4"]
    else:
        hair_btn_c4["state"] = "disabled"
        hair_btn_c4["bg"] = "#d4d4d4"
    update_canvas()


def update_hair_color(cl):
    elem = "hair_" + letters[hair_type - 1] + "_" + cl
    color = askcolor(title=lang["choose_color"], color=colors[elem])
    colors[elem] = (abs(round(color[0][0]-5)), round(abs(color[0][1]-5)), round(abs(color[0][2])-1))
    if cl == "c1":
        hair_btn_c1["bg"] = color[1]
    elif cl == "c2":
        hair_btn_c2["bg"] = color[1]
    elif cl == "c3":
        hair_btn_c3["bg"] = color[1]
    elif cl == "c4":
        hair_btn_c4["bg"] = color[1]
    update_canvas()


hair_frame = LabelFrame(options_frame, text=lang["padoru_hair"], bd=2, background="#FFF0C1", relief="groove")
hair_frame.grid(row=2, column=0, padx=5, pady=5)

hair_values = [lang["padoru_type"] + " A", lang["padoru_type"] + " B", lang["padoru_type"] + " C"]
hair_combo = ttk.Combobox(hair_frame, values=hair_values, state="readonly")
hair_combo.grid(column=0, row=0, padx=5, pady=5)
hair_combo.current(0)
hair_combo.bind("<<ComboboxSelected>>", hair_update)

hair_btn_c1 = Button(hair_frame, text=lang["change_color"], command=lambda: update_hair_color("c1"), bg='#%02x%02x%02x' % colors["hair_" + letters[hair_type - 1] + "_c1"])
hair_btn_c1.grid(column=0, row=1, padx=5, pady=5)

hair_btn_c2 = Button(hair_frame, text=lang["change_color"], command=lambda: update_hair_color("c2"), bg='#%02x%02x%02x' % colors["hair_" + letters[hair_type - 1] + "_c2"])
hair_btn_c2.grid(column=0, row=2, padx=5, pady=5)

hair_btn_c3 = Button(hair_frame, text=lang["change_color"], command=lambda: update_hair_color("c3"), bg='#%02x%02x%02x' % colors["hair_" + letters[hair_type - 1] + "_c3"])
hair_btn_c3.grid(column=0, row=3, padx=5, pady=5)

hair_btn_c4 = Button(hair_frame, text=lang["change_color"], command=lambda: update_hair_color("c4"), bg='#%02x%02x%02x' % colors["hair_" + letters[hair_type - 1] + "_c4"])
hair_btn_c4.grid(column=0, row=4, padx=5, pady=5)


# HAT
def update_hat_color(cl):
    elem = "hat_" + cl
    color = askcolor(title=lang["choose_color"], color=colors[elem])
    colors[elem] = (abs(round(color[0][0]-5)), round(abs(color[0][1]-5)), round(abs(color[0][2])-1))
    if cl == "c1":
        hat_btn_c1["bg"] = color[1]
    elif cl == "c2":
        hat_btn_c2["bg"] = color[1]
    elif cl == "c3":
        hat_btn_c3["bg"] = color[1]
    elif cl == "c4":
        hat_btn_c4["bg"] = color[1]
    update_canvas()


hat_frame = LabelFrame(options_frame, text=lang["padoru_hat"], bd=2, background="#FFF0C1", relief="groove")
hat_frame.grid(row=2, column=1, padx=5, pady=5)

hat_btn_c1 = Button(hat_frame, text=lang["change_color"], command=lambda: update_hat_color("c1"), bg='#%02x%02x%02x' % colors["hat_c1"])
hat_btn_c1.grid(column=0, row=1, padx=5, pady=5)

hat_btn_c2 = Button(hat_frame, text=lang["change_color"], command=lambda: update_hat_color("c2"), bg='#%02x%02x%02x' % colors["hat_c2"])
hat_btn_c2.grid(column=0, row=2, padx=5, pady=5)

hat_btn_c3 = Button(hat_frame, text=lang["change_color"], command=lambda: update_hat_color("c3"), bg='#%02x%02x%02x' % colors["hat_c3"])
hat_btn_c3.grid(column=0, row=3, padx=5, pady=5)

hat_btn_c4 = Button(hat_frame, text=lang["change_color"], command=lambda: update_hat_color("c4"), bg='#%02x%02x%02x' % colors["hat_c4"])
hat_btn_c4.grid(column=0, row=4, padx=5, pady=5)


# BG
def bg_update(event):
    global bg_type
    ind = bg_values.index(event.widget.get())
    bg_type = ind
    if ind == 0:
        bg_btn["state"] = "disabled"
        bg_btn["bg"] = "#d4d4d4"
    else:
        bg_btn["state"] = "normal"
        bg_btn["bg"] = '#%02x%02x%02x' % colors["bg"]
    update_canvas()


def update_bg_color():
    elem = "bg"
    color = askcolor(title=lang["choose_color"], color=colors[elem])
    colors[elem] = (round(abs(color[0][0]-5)), round(abs(color[0][1]-5)), round(abs(color[0][2])-1))
    bg_btn["bg"] = color[1]
    update_canvas()


bg_frame = LabelFrame(options_frame, text=lang["background"], bd=2, background="#FFF0C1", relief="groove")
bg_frame.grid(row=2, column=3, padx=5, pady=5)

bg_values = [lang["background_a"], lang["background_b"]]
bg_combo = ttk.Combobox(bg_frame, values=bg_values, state="readonly")
bg_combo.grid(column=0, row=0, padx=5, pady=5)
bg_combo.current(0)
bg_combo.bind("<<ComboboxSelected>>", bg_update)

bg_btn = Button(bg_frame, text=lang["change_color"], command=update_bg_color, state="disabled", bg="#d4d4d4")
bg_btn.grid(column=0, row=1, padx=5, pady=5)


root.mainloop()
