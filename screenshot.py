from PIL import ImageGrab
import numpy as np

import cv2

def screen_shot():
    printscreen_pil =  ImageGrab.grab()
    # print(printscreen_pil.size)
    printscreen_numpy = np.array(printscreen_pil, dtype="uint8")\
    .reshape((printscreen_pil.size[1],printscreen_pil.size[0],4))
    # print(printscreen_numpy[:,:,:3].shape)
    # cv2.imshow("", printscreen_numpy[:,:,:3])
    # cv2.waitKey(0)
    return printscreen_numpy[:,:,:3]