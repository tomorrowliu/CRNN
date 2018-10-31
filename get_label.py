#coding=utf-8
import os
import pandas as pd
import numpy as np


#获得文件中的图片和数据
def getallfiles(path):
    allfile=[]
    for dirpath,dirnames,filenames in os.walk(path):
        for name in filenames:
            allfile.append(os.path.join(name))
    return allfile

path1 = 'E:/pycharm/workplace/tensorflow/tianci/picture'
allfile1 = getallfiles(path1)
result_all =list()
for picturefile in allfile1:
    path2 = 'E:/pycharm/workplace/tensorflow/tianci/data'
    picture = path1 + '/' + picturefile
    datafile1 = picturefile[:-3]
    datafile = path2 + '/' + datafile1 + 'txt'
    file = open(datafile, 'r',encoding='UTF-8')
    result = list()
    for c in file.readlines():
        c_array = c.split(",")
        result.append(c_array[-1])
    # print(result)
    result_all.append(result)
print(result_all)
print(type(result_all))
f1=open('result.txt','w')
f1.write(','.join(str(num) for num in result_all))
f1.close()
