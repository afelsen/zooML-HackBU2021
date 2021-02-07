from torch.utils.data import Dataset
import glob
import cv2
import numpy as np
# import FaceBox

class FaceDataset(Dataset):
    def __init__(self, path, train):
        self.data = []
        categories = ["attentive", "confused", "inattentive", "sleeping", "talking"]
        for i, category in enumerate(categories):
            for filename in glob.glob(f"{path}/{category}/*/*.png"):
                input = cv2.imread(filename)

                # input_small = FaceBox.processFrame(input)
                # locations = FaceBox.findFaces(input_small)
                # locations *= 4
                # print(locations)

                input = cv2.resize(input, (128,128))

                label = np.zeros((5))
                label[i] = 1
                self.data.append((input, label))
                print(filename, end = '\t\r')

    def __len__(self):
        return len(self.data)
    def __getitem__(self, index):
        return self.data[index]
