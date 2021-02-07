import GUI
import screenShot
import FaceBox
import FaceNetwork

import numpy as np

import cv2


def main():
    gui = GUI.GUI()
    gui.home_page()
    while True:
        gui.root.update()
        gui.root.update_idletasks()
        ss = screenShot.screen_shot()

        transBox = FaceBox.getTransBoxes(ss)
        # print(type(transBox))
        # print(transBox.shape)
        # cv2.imshow("", transBox)
        # cv2.waitKey(0)
        gui.recording(transBox.astype(np.uint8))




main()