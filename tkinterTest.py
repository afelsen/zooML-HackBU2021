import tkinter as tk
import platform
from PIL import Image, ImageTk
import numpy

def main():


    root = tk.Tk()
    root.title("ZooML")
    root.geometry(str(root.winfo_screenwidth()) + "x" + str(root.winfo_screenheight()))
    # root.wm_attributes("-topmost", True)
    home_page()
    general_recording()

    # root.attributes("-alpha", .5)
    # label = tk.Label(root, text = "Spy on your Students").pack()

    root.mainloop()

def home_page():
    pass

def general_recording():
    os = platform.system()

    if os == "Windows":
        img = numpy.zeros((512,512))
        root.image = ImageTk.PhotoImage(Image.fromarray(img))
        label = tk.Label(root, image = root.image, bg = "white")
        root.lift()

        root.wm_attributes("-disabled", True)
        root.wm_attributes("-transparentcolor", "white")
        label.pack()
    elif os == "Darwin": #Macos
        # root.wm_attributes("-transparent", True)
        root.config(bg = "systemTransparent")
        img = numpy.zeros((512,512))
        root.image = ImageTk.PhotoImage(Image.fromarray(img))
        print(type(root.image))
        label = tk.Label(root, image = root.image)
        label.config(bg = "systemTransparent")
        label.pack()

    else:
        print("Unsupported Operating system or operatin system not recognized")
        return

main()
