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
import torch
from FaceNetwork import FaceNetwork

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
    smallFrame = smallFrame[:, :, ::-1] # convert from BGR (used by cv2) to RGB (used by fr)
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

def run_single(net, image, device):
    image = image[np.newaxis, ..., np.newaxis]
    image = torch.from_numpy(image)

    with torch.no_grad():
        image = image.to(device, dtype=torch.float)
        image = image.permute(0, 3, 1, 2)

        output = net(image)

    max, out = torch.max(output.data, 1) # tensor([[-0.0449, -0.0347, -0.3300, -0.0956,  0.0510]])
    print(output.data)

    categories = ["attentive", "confused", "inattentive", "talking"]
    return categories[out]

def getTransBoxes(desktopImage, net, device):
    smallFrame = cv2.resize(desktopImage, (0, 0), fx=0.25, fy=0.25)
    foundLocations = findFaces(smallFrame)

    # GET LABELS FOR EACH FACE FROM ADIEL HERE
    addLabels = []
    for face in foundLocations:
        #print("Face Found!")
        top = face[0] * 4 # scale bounding box back up (was scaled 1/4 earlier for faster processing speed)
        right = face[1] * 4
        bottom = face[2] * 4
        left = face[3] * 4
        faceImg = np.array(desktopImage)[top:bottom, left:right]
        faceImg = cv2.resize(faceImg, (128, 128))
        faceImg = cv2.cvtColor(faceImg, cv2.COLOR_BGR2GRAY)
        label = run_single(net, faceImg, device)

        addLabels.append(label)

    transparentImage = np.zeros((desktopImage.shape[0], desktopImage.shape[1], 4))
    boxedImage = drawBoxes(transparentImage, foundLocations, addLabels=addLabels, boxColor=(255,100,100,255), fontColor=(0,0,0,255), font=cv2.FONT_HERSHEY_DUPLEX)

    #boxedImage = drawBoxes(np.array(desktopImage), foundLocations, addLabels=addLabels, boxColor=(255,100,100), fontColor=(0,0,0), font=cv2.FONT_HERSHEY_DUPLEX)

    #transparentImage = np.zeros((desktopImage.shape[0], desktopImage.shape[1], 3))
    #boxedImage = drawBoxes(np.array(transparentImage), foundLocations, addLabels=addLabels, boxColor=(255,100,100), fontColor=(0,0,0), font=cv2.FONT_HERSHEY_DUPLEX)

    return boxedImage

def cropImage(path, replaceOriginal=False, resize=True):
    frame = cv2.imread(path, cv2.IMREAD_COLOR)
    if resize:
        smallFrame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    else:
        smallFrame = frame
    foundLocations = findFaces(smallFrame)

    if not replaceOriginal:
        # go through cropping out each face
        for i in range(len(foundLocations)):
            if resize:
                top = foundLocations[i][0] * 4 # scale bounding box back up (was scaled 1/4 earlier for faster processing speed)
                right = foundLocations[i][1] * 4
                bottom = foundLocations[i][2] * 4
                left = foundLocations[i][3] * 4
            else:
                top = foundLocations[i][0] # scale bounding box back up (was scaled 1/4 earlier for faster processing speed)
                right = foundLocations[i][1]
                bottom = foundLocations[i][2]
                left = foundLocations[i][3]

            faceImg = frame[top:bottom, left:right]
            cv2.imwrite(path[:path.find(".")] + "_" + str(i) + ".png", faceImg)
    else:
        if resize:
            top = foundLocations[0][0] * 4 # scale bounding box back up (was scaled 1/4 earlier for faster processing speed)
            right = foundLocations[0][1] * 4
            bottom = foundLocations[0][2] * 4
            left = foundLocations[0][3] * 4
        else:
            top = foundLocations[0][0] # scale bounding box back up (was scaled 1/4 earlier for faster processing speed)
            right = foundLocations[0][1]
            bottom = foundLocations[0][2]
            left = foundLocations[0][3]

        faceImg = frame[top:bottom, left:right]
        cv2.imwrite(path, faceImg)

def cropDataset(root="Data/", resize=True):
    for folder in os.listdir(root):
        if folder != ".DS_Store":
            for file in os.listdir(root + folder + "/"):
                if file != ".DS_Store":
                    try:
                        cropImage(root + folder + "/" + file, replaceOriginal=True, resize=resize)
                    except:
                        print("Could Not Find Face: " + root + folder + "/" + file)

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

        # draw bounding boxes on the frame
        frame = drawBoxes(frame, foundLocations, addLabels=foundNames)

        cv2.imshow('Video', frame) # show frame
        if cv2.waitKey(1) & 0xFF == ord('q'): # check for Q keypress (to quit)
            done = True

    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    #test()
    #cropImage("images/input.png")
    cropDataset()
