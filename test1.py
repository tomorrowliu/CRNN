import os
import tensorflow as tf
import pandas as pd
from PIL import Image,ImageDraw
img=Image.open('TB1..FLLXXXXXbCXpXXunYpLFXX.jpg')
draw=ImageDraw.Draw(img)
text_point=pd.read_csv('TB1..FLLXXXXXbCXpXXunYpLFXX.txt',header=None)
for idx,row in text_point.iterrows():
    point=row.loc[range(8)].tolist()
    x=[point[i] for i in [0,2,4,6]]
    y=[point[i] for i in [1,3,5,7]]
    point=[(a,b) for a,b in zip(x,y)]
    draw.polygon(point,outline=(0,128,255))
img.show()
# region=(min(x),min(y),max(x),max(y))
# cropimg=img.crop(region)
# cropimg.show()