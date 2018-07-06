# -*- coding: utf-8 -*-
from __future__ import division
import csv
import os
import math
import numpy as np
import urllib
import json
import urllib.request
import urllib.error

class Preprocess:
    total_word_list = []
    total_word_dict = {}
    total_word_set = []
    TF_IDF_dict = {}
    vec_list = []
    label_list = []
    wordbag = np.zeros([655,1001])

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
                self.label_list.append(class_index)
                index += 1
                with open(foldername, "w", encoding='utf-8') as writeholder:
                    for items in line:
                        writeholder.write(items)
                        writeholder.write(' ')

    def getAccessToken(self):
        print('Get Access Token')
        AK = 'ylCi3zhVArGU4gkS2NzAB0dr'
        SK = 'VEjH2k6stKYValgX5DjvbHVthpELMN3p'
        host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + AK + '&client_secret=' + SK
        request = urllib.request.Request(host)
        request.add_header('Content-Type', 'application/json; charset=UTF-8')
        ATresponse = urllib.request.urlopen(request)
        content = ATresponse.read()
        if (content):
            dic_json = json.loads(content)
            AT = dic_json['access_token']
            return AT
        else:
            return False

    def lexer(self,AT):
        print('Start lexer')
        #print(AT)
        lexer_url = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/lexer' + '?charset=UTF-8&access_token=' + AT
        list_dirs = os.walk("data")
        for root, dirs, files in list_dirs:
            for f in files:
                with open(os.path.join(root, f),'r+',encoding='utf-8') as datafile:
                    str = datafile.read()
                    #print(str)
                    info = {
                        'text': str
                    }
                    dic_info = json.dumps(info)
                    headers = {'Content-Type': 'application/json'}
                    while (1):
                        try:
                            req = urllib.request.Request(url=lexer_url, data=dic_info.encode('gbk'), headers=headers)
                            response = urllib.request.urlopen(req, timeout=5)
                            break
                        except urllib.error.URLError as e:
                            print('except:', e)
                    response = eval(response.read().strip())
                    sinlge_doc_word_list = []
                    for items in response['items']:
                        if (items['pos'] != 'w'):
                            self.total_word_list.append(items['item'])
                            sinlge_doc_word_list.append(items['item'])
                    self.total_word_dict.update({f:sinlge_doc_word_list})
                    print(os.path.join(root, f) + ' finish')
        self.total_word_set = list(set(self.total_word_list))
        '''
        with open('total_word_set.txt','w',encoding='utf-8', errors='ignore') as total_word_set_file:
            for item in self.total_word_set:
                total_word_set_file.writelines(item)
                #total_word_set_file.writelines('\n')
        with open('total_word_list.txt','w',encoding='utf-8', errors='ignore') as total_word_list_file:
            for item in self.total_word_list:
                total_word_list_file.writelines(item)
                #total_word_list_file.writelines('\n')
        '''
    def Save(self):
        with open('wordbag.csv', 'w', encoding='utf-8', errors='ignore') as wordbag_file:
            writer = csv.writer(wordbag_file)
            writer.writerow(self.wordbag)
        with open('total_word_list.csv', 'w', encoding='utf-8', errors='ignore') as label_list_file:
            writer = csv.writer(label_list_file)
            writer.writerow(self.label_list)

    def TF_IDF(self,str):
        single_word_count = 0
        total_word_count = 7494
        TF = 0
        total_doc_count = 655
        contain_doc_count = 0
        IDF = 0
        single_word_count = 0
        for item in self.total_word_list:
            if(item == str):
                single_word_count += 1
        TF = single_word_count/total_word_count
        for title, content_list in self.total_word_dict.items():
            if str in content_list:
                contain_doc_count += 1
        IDF = contain_doc_count/total_doc_count
        #print(str)
        #print(TF*IDF)
        return math.log(TF*IDF)

    def wordbagGenerate(self):
        print('start wordbag generate')
        print('----------------------')
        with open("knowledgeTree.csv", "rU", encoding='gbk') as fileholder:
            reader = csv.reader(fileholder)
            line_index = 0
            for line in reader:
                for item in line:
                    col_index = 0
                    for word in self.total_word_set:
                        if word in item:
                            self.wordbag[line_index][col_index] += 1
                        col_index += 1
                line_index += 1
        print(self.wordbag)
