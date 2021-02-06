import cv2
import numpy as np
import os

def capture_video(path):
    category = None

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    while True:
        ret, frame = cap.read()

        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        if category != None:
            try:
                f = open(f"{path}/{category}/file_num.txt", 'r')
                frame_num = int(f.read())
                f.close()
            except:
                frame_num = 0

            cv2.imwrite(f"{path}/{category}/{frame_num}.png", frame)

            f = open(f"{path}/{category}/file_num.txt", 'w')
            f.write(f"{frame_num + 1}")


        show_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        cv2.imshow('frame', show_frame)


        key = cv2.waitKey(1)
        if key == ord('i'):
            category = "inattentive"
        if key == ord('a'):
            category = "attentive"
        if key == ord('c'):
            category = "confused"
        if key == ord('s'):
            category = "sleeping"
        if key == ord('t'):
            category = "talking"
        if key == -1:
            category = None

        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":

    print("Welcome to zooML data collection system.")
    print(
    "Hold:\n\t"
    "'a' to record yourself attentive\n\t"
    "'i' to record yourself inattentive\n\t"
    "'c' to record yourself confused\n\t"
    "'s' to record yourself sleeping\n\t"
    "'t' to record yourself talking\n\t"
    "'q' to quit"
    )
    name = input("Please type your name to begin: ")


    for category in ["attentive", "inattentive", "confused", "sleeping", "talking"]:
        path = f"./Data/{category}/{name}/"
        try:
            os.mkdir(path)
        except:
            print(f"{path} already exists")

    capture_video("./Data")
