import os
import pandas as pd
from PIL import Image,ImageDraw

#定义文件获取方法 :dirpath,dirnames,filenames 分别是 文件夹路径, 文件夹名字, 文件名，遍历文件夹，获取文件夹内文件名称
def getallfiles(path):
    allfile=[]
    for dirpath,dirnames,filenames in os.walk(path):            #调用 os.walk()方法，遍历所以的文件，并将文件名称赋值给allfile   ：http://www.runoob.com/python/os-walk.html
        for name in filenames:
            allfile.append(os.path.join(name))
    return allfile

#主程序
if __name__ == '__main__':
    # 文件地址，注意区分 ，要用‘/’符号,‘\’无法读取
    path1 = 'E:/pycharm/workplace/tensorflow/tianci/picture'
    path2 = 'E:/pycharm/workplace/tensorflow/tianci/data'
    allfile1 = getallfiles(path1)                                             #调取文件获取方法
    #利用for循环实现遍历读取图片，和文档
    for picturefile in allfile1:
        picture = path1+'/'+picturefile                                 #将每个图片的地址赋给picture
        datafile1 = picturefile[:-3]                                    #只读取图片倒数3位之前值，最后4位是'jpg'，不需要读取
        datafile  = path2+'/'+datafile1+'txt'                          #将每个图片对应的数据文档地址赋给datafile
        img = Image.open(picture)                                      #调用open方法读取picture
        draw = ImageDraw.Draw(img)                                       #调用draw方法， 将图像赋给draw,在后边可以调用polygon对图像进行操作
        data = pd.read_csv(datafile,header=None)                        #调用read_csv方法读取txt文件

        #将数据集中的8个坐标编辑成为 （x0,y1),(x2,y3),(x4,y5),(x6,y7)
        for idx,row in data.iterrows():
            point=row.loc[range(8)].tolist()                        #获取8个坐标数值
            x=[point[i] for i in [0,2,4,6]]                         #分别将 point 中0,2,4,6 这4个列标对应的值给 x 列表
            y=[point[i] for i in [1,3,5,7]]                         #分别将 point 中1,3,5,7 这4个列标对应的值给 y 列表
            point=[(a,b) for a,b in zip(x,y)]                       #从新将 point 变为坐标组合成[（x0,y1),(x2,y3),(x4,y5),(x6,y7)],方法zip()就是把2个数组糅在一起
            draw.polygon(point,outline=(255,255,0))                  #  画图，调用polygon方法画多边形
        img.show()                                                   #  显示图片
