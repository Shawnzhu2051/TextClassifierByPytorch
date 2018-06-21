# -*- coding: utf-8 -*-
import csv
import os
import math
import numpy as np
import urllib
import json
import urllib.request
import urllib.error

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
                    print(str)
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
                        except urllib.error.HTTPError as e:
                            print('except:', e)
                    response = eval(response.read().strip())
                    datafile.truncate(0)
                    for items in response['items']:
                        if (items['pos'] != 'w'):
                            datafile.writelines(items['item'])
                            datafile.writelines('\n')
                    print(os.path.join(root, f) + ' finish')

    def dictGenerate(self):
        pass


    def wordbagGenerate(self):
        pass