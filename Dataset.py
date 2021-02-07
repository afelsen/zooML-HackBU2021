from torch.utils.data import Dataset
import glob
import cv2
import numpy as np
# import FaceBox
import random

class FaceDataset(Dataset):
    def __init__(self, path, train):

        self.data = []

        cat_data = {}
        categories = ["attentive", "confused", "inattentive", "talking"]
        for i, category in enumerate(categories):
            cat_data[category] = []
            for filename in glob.glob(f"{path}/{category}/*/*.png"):
                input = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)

                input = cv2.resize(input, (128,128))

                input = input[..., np.newaxis]

                label = np.zeros((5))
                label[i] = 1
                cat_data[category].append((input, label))
                print(filename, end = '\t\r')

        random.seed(324948032)

        max_size = min([len(v) for v in cat_data.values()])

        for category in categories:
            single_cat_data = cat_data[category]
            random.shuffle(single_cat_data)
            single_cat_data = single_cat_data[:max_size]

            if train:
                single_cat_data = single_cat_data[:int(len(single_cat_data)*.8)]
            else:
                single_cat_data = single_cat_data[int(len(single_cat_data)*.8):]

            self.data += single_cat_data

        print()
        print(len(self.data))

    def __len__(self):
        return len(self.data)
    def __getitem__(self, index):
        return self.data[index]
