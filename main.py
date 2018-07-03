from __future__ import print_function
import Preprocess
import os
import csv
from Model import Net
import numpy as np
import torch
from torch.autograd import Variable
import torch.nn.functional as F


if __name__ == '__main__':

    preprcess = Preprocess.Preprocess()
    path = "data/"
    isPathExit = os.path.exists(path)

    if (os.path.exists('wordbag.txt')):
        with open('wordbag.csv', 'r', encoding='utf-8', errors='ignore') as wordbag_file:
            reader = csv.reader(wordbag_file)
            for item in reader:
                preprcess.wordbag.append(item)
        with open('total_word_list.csv', 'r', encoding='utf-8', errors='ignore') as label_list_file:
            reader = csv.reader(label_list_file)
            for item in reader:
                preprcess.label_list.append(item)
    else:
        if not isPathExit:
            preprcess.datasetPrepare()
            print("build success")
            AT = preprcess.getAccessToken()
            preprcess.lexer(AT)
        else:
            print("build already finish")
        for item in preprcess.total_word_set:
            preprcess.TF_IDF_dict[item] = preprcess.TF_IDF(item)
        print(preprcess.TF_IDF_dict)
        preprcess.wordbagGenerate()
        preprcess.Save()


    print('wordbag: ')
    print(preprcess.wordbag)
    print('label_list: ')
    print(preprcess.label_list)


    x = np.array(preprcess.wordbag)
    y = np.array(preprcess.label_list)
    x = torch.from_numpy(x).type(torch.FloatTensor)
    y = torch.from_numpy(y)
    x, y = Variable(x), Variable(y)

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

