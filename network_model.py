# -*- coding: utf-8 -*-

from pytesser.pytesser import image_to_string

from PIL import *
import  Image
import ImageEnhance

image =Image.open(r"TB2965Lb46I8KJjSszfXXaZVXXa_!!646445699.jpg.jpg")
enhancer =ImageEnhance.Contrast(image)
image_enhancer =enhancer.enhance(4)

print(image_to_string(image_enhancer))