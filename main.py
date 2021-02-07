import GUI
import screenShot
import FaceBox
import FaceNetwork
import numpy as np
import cv2

def do_update():
    FACTOR = 1

    ss = screenShot.screen_shot()
    transBox = FaceBox.getTransBoxes(ss)
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
# gui.home_page()
gui.recording_setup()
gui.root.after(1, call_periodically)
gui.root.mainloop()
