import os
import pandas as pd
from pandas import *
import cv2
import numpy as np
from math import *
from random import *

#获得文件中的图片和数据
def getallfiles(path):
    allfile=[]
    for dirpath,dirnames,filenames in os.walk(path):
        for name in filenames:
            allfile.append(os.path.join(name))
    return allfile

#对图像进行旋转、仿射
def rotateImage(img,degree,pt1,pt2,pt3,pt4,d,z):
    height,width=img.shape[:2]
    heightNew = int(width * fabs(sin(radians(degree))) + height * fabs(cos(radians(degree))))
    widthNew = int(height * fabs(sin(radians(degree))) + width * fabs(cos(radians(degree))))
    matRotation=cv2.getRotationMatrix2D((width/2,height/2),degree,1)
    matRotation[0, 2] += (widthNew - width) / 2
    matRotation[1, 2] += (heightNew - height) / 2
    imgRotation = cv2.warpAffine(img, matRotation, (widthNew, heightNew), borderValue=(255, 255, 255))
    pt1 = list(pt1)
    pt2 = list(pt2)
    pt3 = list(pt3)
    pt4 = list(pt4)
    [[pt1[0]], [pt1[1]]] = np.dot(matRotation, np.array([[pt1[0]], [pt1[1]], [1]]))
    [[pt2[0]], [pt2[1]]] = np.dot(matRotation, np.array([[pt2[0]], [pt2[1]], [1]]))
    [[pt3[0]], [pt3[1]]] = np.dot(matRotation, np.array([[pt3[0]], [pt3[1]], [1]]))
    [[pt4[0]], [pt4[1]]] = np.dot(matRotation, np.array([[pt4[0]], [pt4[1]], [1]]))
    imgOut=imgRotation[int(pt1[1]):int(pt3[1]),int(pt1[0]):int(pt3[0])]   #文本图片
    s=np.array(imgOut)
    shape=s.shape
    h=shape[0]
    h1=shape[1]
    h2=shape[2]
    j=h*h1*h2

    df.loc[d] = [imgOut,z,shape]
    if j:
        res = cv2.resize(imgOut, (500, 500), interpolation=cv2.INTER_CUBIC)
        s = np.array(res)
        shape = s.shape
        Tdf.loc[d] = [res, z, shape]
    filename=str(ct)+'.jpg'
    if len(imgOut)!=0:


        cv2.imwrite(filename,imgOut)
    return imgRotation,imgOut,df,Tdf

#画出外接框
def drawRect(img,pt1,pt2,pt3,pt4,color,lineWidth):
    cv2.line(img, pt1, pt2, color, lineWidth)
    cv2.line(img, pt2, pt3, color, lineWidth)
    cv2.line(img, pt3, pt4, color, lineWidth)
    cv2.line(img, pt1, pt4, color, lineWidth)

#求得旋转角度
def getct(x,y):
    rows1 = int(x[1])
    cols1 = int(y[1])
    rows2 = int(x[2])
    cols2 = int(y[2])
    try:
        h = (cols2 - cols1) / (rows2 - rows1)
    except ValueError as e:
        print(e)
    except ZeroDivisionError as e:
        print(e)
    cta = degrees(atan(h))
    return cta


if __name__ == '__main__':
    path1='D:/aliyun/code/picture'
    allfile1=getallfiles(path1)
    d=-1
    b=0
    c=0
    df = DataFrame(columns=['data','label','shape'])
    Tdf = DataFrame(columns=['data','label','shape'])
    for picturefile in allfile1:
        path2 = 'D:/aliyun/code/data'
        picture = path1 + '/' + picturefile
        datafile1 = picturefile[:-3]
        datafile = path2 + '/' + datafile1 + 'txt'
        img = cv2.imread(picture)
        if img!=None:
            print(picture)
            data = pd.read_csv(datafile, header=None)
            for idx, row in data.iterrows():
                d = d + 1
                point = row.loc[range(9)].tolist()
                x = [point[i] for i in [0, 2, 4, 6]]
                y = [point[i] for i in [1, 3, 5, 7]]
                z = [point[i] for i in [8]]
                point = [(a, b) for a, b in zip(x, y)]
                ct = getct(x, y)
                imgRotation, a ,Dimg,TD= rotateImage(img, -ct, point[0], point[1], point[2], point[3],d,z)
                if len(a) != 0:
                    b = b + 1
                elif len(a) == 0:
                    c = c + 1
        print('成功截取的图像数'+str(b)+'没有成功截取的图像数'+str(c))
    # Dimg.to_excel('Dimg.xlsx')
    TD.to_excel('TD.xlsx')













