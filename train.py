from FaceNetwork import FaceNetwork
from Dataset import FaceDataset

import torch
import cv2
import numpy as np


def train(net, traindata, device):
    criterion = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(net.parameters(), lr=0.07)

    for epoch in range(25):
        running_loss = 0
        running_accuracy = 0
        for i, data in enumerate(traindata, 0):
            inputs, labels = data[0].to(device=device, dtype=torch.float), data[1].to(device=device, dtype=torch.long)
            inputs = inputs.permute(0, 3, 1, 2)

            labels = labels.argmax(1)
            outputs = net(inputs)

            loss = criterion(outputs, labels)
            loss.backward()

            total = labels.size(0)
            _, outputs = torch.max(outputs.data, 1)
            correct = (outputs == labels).sum().item()
            running_accuracy += correct / total

            optimizer.step()
            optimizer.zero_grad()

            running_loss += loss.item()

            print(f"Running loss: {running_loss/(i+1):.3f}\tRunning Accuracy: {running_accuracy/(i+1)}", end = '\r')
        print()

    print("Saving model...")
    PATH = "Models/test_2.pth"
    torch.save({
        'epoch': epoch,
        'model_state_dict': net.state_dict(),
        'optimizer_state_dict': optimizer.state_dict(),
        'loss': loss
    }, PATH)

def test(net, testloader, device):
    net = FaceNetwork().to(device)
    checkpoint = torch.load("./Models/test_2.pth")
    net.load_state_dict(checkpoint['model_state_dict'])

    running_accuracy = 0
    with torch.no_grad():
        for data in testloader:
            inputs, labels = data[0].to(device=device, dtype=torch.float), data[1].to(device=device, dtype=torch.float)
            inputs = inputs.permute(0, 3, 1, 2)

            labels = labels.argmax(1)
            outputs = net(inputs)

            total = labels.size(0)
            _, outputs = torch.max(outputs.data, 1)
            correct = (outputs == labels).sum().item()
            running_accuracy += correct / total



    print(f"testing accuracy: {running_accuracy / len(testloader)}")

def test_single(net, image):
    checkpoint = torch.load("./Models/test_2.pth")
    net.load_state_dict(checkpoint['model_state_dict'])

    net.eval()

    image = image[np.newaxis, ..., np.newaxis]
    image = torch.from_numpy(image)
    print(image.shape)

    with torch.no_grad():
        image = image.to(device, dtype=torch.float)
        image = image.permute(0, 3, 1, 2)

        output = net(image)

        print(output)


if __name__ == "__main__":
    net = FaceNetwork()
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    net.to(device)

    traindata = FaceDataset("./Data_all", train = True)
    trainloader = torch.utils.data.DataLoader(traindata, batch_size = 4, shuffle = True, num_workers = 4)

    testdata = FaceDataset("./Data_all", train = False)
    testloader = torch.utils.data.DataLoader(traindata, batch_size = 4, shuffle = False, num_workers = 4)

    train(net, trainloader, device)
    test(net, testloader, device)

    for i in range(10):
        image = cv2.imread(f"Nick_Data/inattentive/{i}.png", cv2.IMREAD_GRAYSCALE)
        test_single(net, image)
