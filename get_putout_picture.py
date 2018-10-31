import os
import pandas as pd
import cv2
import numpy as np
from math import *

#定义文件获取方法 :dirpath,dirnames,filenames 分别是 文件夹路径, 文件夹名字, 文件名，遍历文件夹，获取文件夹内文件名称
def getallfiles(path):
    allfile=[]
    for dirpath,dirnames,filenames in os.walk(path):
        for name in filenames:
            allfile.append(os.path.join(name))
    return allfile

#对图片进行反转
def rotateImage(img,degree,pt1,pt2,pt3,pt4):
    height,width=img.shape[:2] #输出图像的大小（x,y）
    # print(img.shape[:2])
    heightNew = int(width * fabs(sin(radians(degree))) + height * fabs(cos(radians(degree))))
    widthNew = int(height * fabs(sin(radians(degree))) + width * fabs(cos(radians(degree))))
    #j矩阵旋转，以图片中心点为中心旋转
    matRotation=cv2.getRotationMatrix2D((width/2,height/2),degree,1)   #参数1 旋转中心，参数2 旋转角度，参数3 缩放大小
    print(matRotation[0, 2])
    # print(matRotation[1, 2])
    matRotation[0, 2] += (widthNew - width) /  2
    matRotation[1, 2] += (heightNew - height) /  2
    print(matRotation[0, 2])
    #得到最后的图像，边界为白色
    imgRotation = cv2.warpAffine(img, matRotation, (widthNew, heightNew), borderValue=(255, 255, 255))

    pt1 = list(pt1)
    pt3 = list(pt3)
    [[pt1[0]], [pt1[1]]] = np.dot(matRotation, np.array([[pt1[0]], [pt1[1]], [1]]))
    [[pt3[0]], [pt3[1]]] = np.dot(matRotation, np.array([[pt3[0]], [pt3[1]], [1]]))
    imgOut=imgRotation[int(pt1[1]):int(pt3[1]),int(pt1[0]):int(pt3[0])]

    filename=str(ct)+'.jpg'
    cv2.imwrite(filename,imgOut)
    return imgRotation

#此处并未调用，圈出矩形
def drawRect(img,pt1,pt2,pt3,pt4,color,lineWidth):
    cv2.line(img, pt1, pt2, color, lineWidth)
    cv2.line(img, pt2, pt3, color, lineWidth)
    cv2.line(img, pt3, pt4, color, lineWidth)
    cv2.line(img, pt1, pt4, color, lineWidth)


if __name__ == '__main__':
    path1='E:/pycharm/workplace/tensorflow/tianci/picture'
    path2='E:/pycharm/workplace/tensorflow/tianci/data'
    # 获取文件地址
    allfile1=getallfiles(path1)
    #遍历对照片和文件进行操作
    for picturefile in allfile1:
        picture=path1+'/'+picturefile
        datafile1=picturefile[:-3]
        datafile=path2+'/'+datafile1+'txt'
        img=cv2.imread(picture)                         #读取图片
        data = pd.read_csv(datafile, header=None)       #读取txt

        for idx, row in data.iterrows():
            point = row.loc[range(8)].tolist()
            x = [point[i] for i in [0, 2, 4, 6]]
            y = [point[i] for i in [1, 3, 5, 7]]
            point = [(a, b) for a, b in zip(x, y)]
            rows1 = int(x[1])                                               #图像 坐标 左下角（x0,y0),左上角（x1,y1）,右上角（x2,y2）,右下角（x3,y3）
            cols1 = int(y[1])
            rows2 = int(x[2])
            cols2 = int(y[2])
            # 求斜率
            h = (cols2 - cols1) / (rows2 - rows1)
            ct = degrees(atan(h))
            #调用rotateImage（）方法，将图片进行反转
            imgRotation = rotateImage(img, -ct, point[0], point[1], point[2], point[3]) #需要的参数是，img调取图片，-ct斜率，以及point[0-3]，4个坐标点位置
