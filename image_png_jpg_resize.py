#分辨率调为256*256,并将png改为jpg

import os
from PIL import Image
import glob
import cv2 as cv

img_path = glob.glob("aligned/*.png")
w=256
h=256
for file in img_path:
    img = cv.imread(file,0)
    print(img.shape)
    ori_w,ori_h = img.shape[::-1]
    print(img.shape, ori_w,ori_h)
    outfile = os.path.splitext(file)[0]+'.jpg'
    print(outfile)
    img=Image.open(file)
    img=img.resize((w,h),Image.ANTIALIAS)
    try:
      if len(img.split())==4:
        r,g,b,a=img.split()
        img=Image.merge("RGB",(r,g,b))
        img.convert("RGB").save(outfile,quality=100)
        os.remove(file)
      else:
        img.convert("RGB").save(outfile,quality=100)
        os.remove(file)
    except Exception as e:
      print(e)
