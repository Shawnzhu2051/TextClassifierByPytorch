# -*- coding: utf-8 -*-
import torch
import torch.nn as nn
from torch.autograd import Variable
import torch.nn.functional as F
import matplotlib.pyplot as plt

n_data = torch.ones(1, 1001)
x = torch.normal(31 * n_data, 1)
y = torch.ones(1).type(torch.LongTensor) * 31
for arg1 in range(31):
    for arg2 in range(21):
        x0 = torch.normal(arg1 * n_data, 1)
        y0 = torch.ones(1).type(torch.LongTensor) * arg1
        x = torch.cat((x, x0), 0).type(torch.FloatTensor)
        y = torch.cat((y, y0), 0).type(torch.LongTensor)

x, y = Variable(x), Variable(y)

class Net(torch.nn.Module):

    def __init__(self):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(1001, 1024)
        self.fc2 = nn.Linear(1024, 256)
        self.fc3 = nn.Linear(256, 32)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x


net = Net()

optimizer = torch.optim.ASGD(net.parameters(), lr=0.002)
criterion = torch.nn.CrossEntropyLoss()

for t in range(10000):
    out = net(x)
    loss = criterion(out, y)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if t % 100 == 0:
        prediction = torch.max(F.softmax(out), 1)[1]
        pred_y = prediction.data.numpy().squeeze()
        target_y = y.data.numpy()
        accuracy = sum(pred_y == target_y) / 652
        print('------------------')
        print('epoch:' + str(t))
        print('loss:' + str(loss))
        print('acc: ' + str(accuracy))
