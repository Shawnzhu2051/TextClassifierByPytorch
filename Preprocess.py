# -*- coding: utf-8 -*-
import csv
import os
import codecs


class Preprocess:
    def __init__(self):
        pass

    def datasetPrepare(self):
        with open("knowledgeTree.csv", "rU", encoding='gbk') as fileholder:
            reader = csv.reader(fileholder)
            index = 0
            class_index = 0
            for line in reader:
                path = "data/" + str(class_index) + '_' + str(line[0])
                isExists = os.path.exists(path)
                if not isExists:
                    class_index += 1
                    path = "data/" + str(class_index) + '_' + str(line[0])
                    os.makedirs(path)
                else:
                    pass
                foldername = path + "/text_" + str(index) + ".txt"
                index += 1
                with open(foldername, "w", encoding='utf-8') as writeholder:
                    for items in line:
                        writeholder.write(items)

    def split(self):
        pass


