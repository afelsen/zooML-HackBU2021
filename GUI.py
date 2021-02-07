import tkinter as tk
import tkinter.font
from tkinter import ttk
import platform
from PIL import Image, ImageTk
import numpy
import json
import cv2


class GUI:
    def __init__(self):

        self.root = tk.Tk()
        self.root.title("ZooML")
        self.root.geometry(str(int(self.root.winfo_screenwidth()/2)) + "x" + str(int(self.root.winfo_screenheight()/2)))
        self.label_font = tkinter.font.Font(family='Arial', size=25)
        self.root.option_add("*Font", self.label_font)

        self.attentive_state = tk.BooleanVar()
        self.confused_state = tk.BooleanVar()
        self.inattentive_state = tk.BooleanVar()
        self.sleeping_state = tk.BooleanVar()
        self.talking_state = tk.BooleanVar()

        self.attentive = tk.Checkbutton(self.root, text="Attentive", var=self.attentive_state, font=self.label_font, bg="black", fg="red", command=self.change_color)
        self.confused = tk.Checkbutton(self.root, text="Confused", var=self.confused_state, font=self.label_font, bg="black", fg="red", command=self.change_color)
        self.inattentive = tk.Checkbutton(self.root, text="Inattentive", var=self.inattentive_state, font=self.label_font, bg="black", fg="red", command=self.change_color)
        self.sleeping = tk.Checkbutton(self.root, text="Sleeping", var=self.sleeping_state, font=self.label_font, bg="black", fg="red", command=self.change_color)
        self.talking = tk.Checkbutton(self.root, text="Talking", var=self.talking_state, font=self.label_font, bg="black", fg="red", command=self.change_color)


        comboStyle = ttk.Style()
        comboStyle.theme_create('combostyle', parent='alt', settings =
                                    {'TCombobox':
                                     {'configure':
                                      {'selectbackground': 'gray13',
                                       'fieldbackground': 'gray13',
                                       'background': 'green'
                                       }}}
                         )
        comboStyle.theme_use('combostyle')
        self.color = ttk.Combobox(self.root, foreground="green")
        # print(comboStyle.element_options("Combobox.padding"))

        # self.root.wm_attributes("-topmost", True)


        # self.root.attributes("-alpha", .5)
        # label = tk.Label(self.root, text = "Spy on your Students").pack()

    def change_color(self):
        if self.attentive_state.get():
            self.attentive['fg'] = 'green'
        else:
            self.attentive['fg'] = 'red'

        if self.confused_state.get():
            self.confused['fg'] = 'green'
        else:
            self.confused['fg'] = 'red'

        if self.inattentive_state.get():
            self.inattentive['fg'] = 'green'
        else:
            self.inattentive['fg'] = 'red'

        if self.sleeping_state.get():
            self.sleeping['fg'] = 'green'
        else:
            self.sleeping['fg'] = "red"

        if self.talking_state.get():
            self.talking['fg'] = 'green'
        else:
            self.talking['fg'] = 'red'


    def home_page(self):

        settings_dict = {}
        with open("settings.json", 'r') as settings:
            settings_dict = json.load(settings)

        self.root.config(bg="black")


        start = tk.Button(self.root, text="Start", command=self.close_settings, fg="white", highlightbackground="gray13",highlightthickness=50, font=self.label_font, )
        start.place(x=450,y=150,width=125,height=50)

        categories = tk.Label(self.root, text="Choose categories to display", font=self.label_font, bg="black", fg="white", justify="left")
        categories.grid(row=0, column = 0)

        self.attentive_state.set(settings_dict["attentive"])
        self.attentive.grid(row=2,column=0, sticky = 'w')

        self.confused_state.set(settings_dict["confused"])
        self.confused.grid(row=4,column=0, sticky = 'w')

        self.inattentive_state.set(settings_dict["inattentive"])
        self.inattentive.grid(row=6,column=0, sticky = 'w')

        self.sleeping_state.set(settings_dict["sleeping"])
        self.sleeping.grid(row=8,column=0, sticky = 'w')

        self.talking_state.set(settings_dict["talking"])
        self.talking.grid(row=10,column=0, sticky = 'w')

        self.change_color()


        colors = ("red", "orange", "yellow", "green", "blue", "indigo", "purple")
        self.color['values'] = colors
        for i in range(len(colors)):
            if colors[i] == settings_dict["color"]:
                self.color.current(i)
        self.color.place(x=300,y=50,width=90,height=30)


    def close_settings(self):
        settings_dict = {}
        settings_dict["attentive"] = self.attentive_state.get()
        settings_dict["confused"] = self.confused_state.get()
        settings_dict["inattentive"] = self.inattentive_state.get()
        settings_dict["sleeping"] = self.sleeping_state.get()
        settings_dict["talking"] = self.talking_state.get()
        settings_dict["color"] = self.color.get()

        jsonString = json.dumps(settings_dict)
        with open("settings.json", 'w') as settings:
            settings.write(jsonString)
        self.attentive.grid_forget()
        self.confused.grid_forget()
        self.inattentive.grid_forget()
        self.sleeping.grid_forget()
        self.talking.grid_forget()

        self.recording_setup()

    def recording_setup(self):
        self.root.destroy()
        self.root = tk.Tk()
        self.root.title("ZooML")
        self.root.geometry(str(self.root.winfo_screenwidth()) + "x" + str(self.root.winfo_screenheight()))


    def recording(self, transBox):

        os = platform.system()

        if os == "Windows":
            img = numpy.zeros((512,512))
            self.root.image = ImageTk.PhotoImage(Image.fromarray(img))
            label = tk.Label(self.root, image=self.root.image, bg="white")
            self.root.lift()

            self.root.wm_attributes("-disabled", True)
            self.root.wm_attributes("-transparentcolor", "white")
            label.pack()
        elif os == "Darwin": #Macos
            self.root.wm_attributes("-transparent", True)
            self.root.config(bg="systemTransparent")
            self.root.image = ImageTk.PhotoImage(Image.fromarray(transBox))
            label = tk.Label(self.root, image=self.root.image)
            label.config(bg="systemTransparent")
        else:
            print("Unsupported Operating system or operatin system not recognized")
            return

