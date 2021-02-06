# Nick's Facial Recognition Wrapper File Inator 2000 2021 Version 3.7.69
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Installation & Usage Instructions
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Step #1: Run: pip3 install opencv-python
# Step #2: Run: pip3 install face-recognition
# Step #3: Run: python3 main.py
# Step #4: Profit
# -=-=-=-=-=-=-=-=-
import face_recognition as fr
import numpy as np
import cv2
import os

def loadEncodings(folder="known_faces/"):
    # Parallel Lists: names[i] is linked to encodings[i] for all i in range(len(names))
    names = []
    encodings = []

    # Load encodings from folder
    for name in os.listdir(folder):
        try: # if the file does have a face to find
            img = fr.load_image_file(folder + name)
            encoding = fr.face_encodings(img)[0]
            names.append(name[:name.find(".")]) # removes ".jpg" from the end of the name
            encodings.append(encoding)
        except: # if not
            print("Skipped Image:", name)

    return names, encodings

def getFrame(camera):
    _, frame = camera.read() # grab video frame
    return frame

def processFrame(frame):
    smallFrame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25) # resize to 1/4 size (processes faster)
    smallFrame = smallFrame[:, :, ::-1] # convert from BGR (used by v2) to RGB (used by fr)
    return smallFrame

def findFaces(frame):
    return fr.face_locations(frame)

def recognizeFaces(frame, foundLocations, knownEncodings, knownNames):
    foundEncodings = fr.face_encodings(frame, foundLocations)
    foundNames = []

    for currentFace in foundEncodings:
        matches = fr.compare_faces(knownEncodings, currentFace)
        currentName = "Unknown"

        # Track down the best match
        faceDistances = fr.face_distance(knownEncodings, currentFace)
        bestMatch = np.argmin(faceDistances) # find which match is closest to the currentFace
        if matches[bestMatch]:
            currentName = knownNames[bestMatch]

        foundNames.append(currentName)
    return foundNames

def drawBoxes(frame, foundLocations, addLabels=None, boxColor=(255,100,100), fontColor=(255, 255, 255), font=cv2.FONT_HERSHEY_SIMPLEX):
    # NOTE: Box Color and Font Color are in BGR

    for i in range(len(foundLocations)):
        top = foundLocations[i][0] * 4 # scale bounding box back up (was scaled 1/4 earlier for faster processing speed)
        right = foundLocations[i][1] * 4
        bottom = foundLocations[i][2] * 4
        left = foundLocations[i][3] * 4

        cv2.rectangle(frame, (left, top), (right, bottom), boxColor, 2) # draw bounding box

        if addLabels != None: # add labels (if they exist)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), boxColor, cv2.FILLED)
            cv2.putText(frame, addLabels[i], (left + 6, bottom - 6), font, 1.0, fontColor, 1)

    return frame

def test():
    camera = cv2.VideoCapture(0)
    knownNames, knownEncodings = loadEncodings()
    done = False

    while not done:
        frame = getFrame(camera)
        smallFrame = processFrame(frame)
        foundLocations = []
        foundNames = []

        foundLocations = findFaces(smallFrame)
        foundNames = recognizeFaces(smallFrame, foundLocations, knownEncodings, knownNames)

        # Draw bounding boxes on the frame
        frame = drawBoxes(frame, foundLocations, addLabels=foundNames)

        cv2.imshow('Video', frame) # show frame
        if cv2.waitKey(1) & 0xFF == ord('q'): # check for Q keypress (to quit)
            done = True

    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    test()
