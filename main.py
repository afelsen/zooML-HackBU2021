from FaceNetwork import FaceNetwork
from Dataset import FaceDataset


def train(net, traindata, device):
    criterion = torch.nn.CrossEntropyLoss()
    optimizer = Adam(net.parameters(), lr=0.07)

    for epoch in range(50):
        for i, data in enumerate(traindata, 0):
            inputs, labels = data[0].to(device=device, dtype=torch.float), data[1].to(device=device, dtype=torch.long)

            outputs = net(inputs)

            loss = criterion(outputs, labels)
            loss.backward()

            optimizer.step()
            optimizer.zero_grad()

            running_loss = loss.item()

            print(f"Running loss: {running_loss:.3f}", end = '\r')


if __name__ == "__main__":
    net = FaceNetwork()
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    net.to(device)

    traindata = FaceDataset(train = True)

    trainloader = torch.utils.data.DataLoader(traindata, batch_size = 4, shuffle = True, num_workers = 4)
