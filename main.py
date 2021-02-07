import GUI
import screenShot
import FaceBox
import numpy as np
import cv2
import torch
from FaceNetwork import FaceNetwork

def do_update():
    FACTOR = 0.5

    ss = screenShot.screen_shot()

    transBox = FaceBox.getTransBoxes(ss, net, device)
    transBox = cv2.resize(transBox, (0, 0), fx=FACTOR, fy=FACTOR)

    #cv2.imwrite("images/output2.png", transBox)
    # print(type(transBox))
    # print(transBox.shape)
    # cv2.imshow("", transBox)
    # cv2.waitKey(0)
    gui.recording(transBox.astype(np.uint8))

def call_periodically():
    print("call periodically")
    do_update()
    gui.root.after(30, call_periodically)


gui = GUI.GUI()
gui.home_page()
# gui.recording_setup()

net = FaceNetwork()
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
net.to(device)
checkpoint = torch.load("./Models/test.pth",map_location=torch.device('cpu'))
net.load_state_dict(checkpoint['model_state_dict'])
net.eval()

gui.root.after(1, call_periodically)
gui.root.mainloop()
