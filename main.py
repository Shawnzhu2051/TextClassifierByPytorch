from __future__ import print_function
import torch
import torch.nn as nn
import torch.nn.functional as F
import Preprocess
import os

'''
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 6, 5)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16*5*5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x):
        x = F.max_pool2d(F.relu(self.conv1(x)), (2, 2))
        x = F.max_pool2d(F.relu(self.conv2(x)), 2)
        x = x.view(-1, self.num_flat_features(x))
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

    def um_flat_features(self, x):
        size = x.size()[1:]
        num_features = 1
        for s in size:
            num_features *= s
        return num_features

net = Net()
print(net)
params = list(net.parameters())
print(len(params))
print(params[0].size())
'''
if __name__ == '__main__':
    preprcess = Preprocess.Preprocess()
    path = "data/"
    isPathExit = os.path.exists(path)
    if not isPathExit:
        preprcess.datasetPrepare()
        print(preprcess.label_list)
        print("build success")
        AT = preprcess.getAccessToken()
        preprcess.lexer(AT)
    else:
        print("build already finish")
    if(len(preprcess.total_word_set) == 0):
        preprcess.ifSave()
    for item in preprcess.total_word_set:
        preprcess.TF_IDF_dict[item] = preprcess.TF_IDF(item)
    print(preprcess.TF_IDF_dict)
    print(len(preprcess.TF_IDF_dict))
