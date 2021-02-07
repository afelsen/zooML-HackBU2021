import tkinter as tk
import tkinter.font
import platform
from PIL import Image, ImageTk
import numpy
import json

class GUI:
    def __init__(self):

        self.root = tk.Tk()
        self.root.title("ZooML")
        self.root.geometry(str(self.root.winfo_screenwidth()) + "x" + str(self.root.winfo_screenheight()))

        self.label_font = tkinter.font.Font(family='Arial', size=25)

        self.attentive_state = tk.BooleanVar()
        self.confused_state = tk.BooleanVar()
        self.inattentive_state = tk.BooleanVar()
        self.sleeping_state = tk.BooleanVar()
        self.talking_state = tk.BooleanVar()

        # self.root.wm_attributes("-topmost", True)


        # self.root.attributes("-alpha", .5)
        # label = tk.Label(self.root, text = "Spy on your Students").pack()




    def home_page(self):

        settings_dict = {}
        with open("settings.json", 'r') as settings:
            settings_dict = json.load(settings)

        self.root.config(bg = "black")

        categories = tk.Label(self.root, text="Choose categories to display", font = self.label_font, bg = "black", fg = "green", justify="left")
        categories.grid(row=0, column = 0)

        self.attentive_state.set(settings_dict["attentive"])
        attentive = tk.Checkbutton(self.root, text = "Attentive", var = self.attentive_state, font = self.label_font, bg = "black", fg = "green")
        attentive.grid(row=2,column=0)

        self.confused_state.set(settings_dict["confused"])
        confused = tk.Checkbutton(self.root, text = "Confused", var = self.confused_state, font = self.label_font, bg = "black", fg = "green")
        confused.grid(row=4,column=0)

        self.inattentive_state.set(settings_dict["inattentive"])
        inattentive = tk.Checkbutton(self.root, text = "Inattentive", var = self.inattentive_state, font = self.label_font, bg = "black", fg = "green")
        inattentive.grid(row=6,column=0)

        self.sleeping_state.set(settings_dict["sleeping"])
        sleeping = tk.Checkbutton(self.root, text = "Sleeping", var = self.sleeping_state, font = self.label_font, bg = "black", fg = "green")
        sleeping.grid(row=8,column=0)

        self.talking_state.set(settings_dict["talking"])
        talking = tk.Checkbutton(self.root, text = "Talking", var = self.talking_state, font = self.label_font, bg = "black", fg = "green")
        talking.grid(row=10,column=0)



    def close_settings(self):
        settings_dict = {}
        settings_dict["attentive"] = self.attentive_state.get()
        settings_dict["confused"] = self.confused_state.get()
        settings_dict["inattentive"] = self.inattentive_state.get()
        settings_dict["sleeping"] = self.sleeping_state.get()
        settings_dict["talking"] = self.talking_state.get()
        jsonString = json.dumps(settings_dict)
        with open("settings.json", 'w') as settings:
            settings.write(jsonString)
        # attentive.pack_forget()
        # confused.pack_forget()
        # inattentive.pack_forget()
        # sleeping.pack_forget()
        # talking.pack_forget()


    def general_recording(self):
        os = platform.system()

        if os == "Windows":
            img = numpy.zeros((512,512))
            self.root.image = ImageTk.PhotoImage(Image.fromarray(img))
            label = tk.Label(self.root, image = self.root.image, bg = "white")
            self.root.lift()

            self.root.wm_attributes("-disabled", True)
            self.root.wm_attributes("-transparentcolor", "white")
            label.pack()
        elif os == "Darwin": #Macos
            # self.root.wm_attributes("-transparent", True)
            self.root.config(bg = "systemTransparent")
            img = numpy.zeros((512,512))
            self.root.image = ImageTk.PhotoImage(Image.fromarray(img))
            print(type(self.root.image))
            label = tk.Label(self.root, image = self.root.image)
            label.config(bg = "systemTransparent")
            label.pack()
        else:
            print("Unsupported Operating system or operatin system not recognized")
            return

def main():
    gui = GUI()
    gui.home_page()
    gui.root.mainloop()

main()