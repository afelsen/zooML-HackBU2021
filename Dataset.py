from torch.utils.data import Dataset
import glob

class FaceDataset(Dataset):
    def __init__(self, train):
        self.data = []
        pass
    def __len__(self):
        return len(self.data)
    def __getitem__(self, index):
        return self.data[index]
