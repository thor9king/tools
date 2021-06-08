'''
压缩，调整大小，改格式
'''


import os
from PIL import Image
import glob
import cv2 as cv

'''CONFIG'''
img_path = glob.glob("/p/ai/vc/stylegan2-ada-pytorch-main/ffhq_out/*.png")

files_out_dir=''#调整后的图片存储路径
w=1024 #调整后的图片宽
h=1024 #调整后的图片高
mb=150 #调整后的图片大小，多少K
step=10 #每次调整的压缩比率
quality=80 #初始压缩比率


def get_size(file):
    # 获取文件大小:KB
    size = os.path.getsize(file)
    return size / 1024
    

def compress_image(infile, mb=150, step=10, quality=80):
    """不改变图片尺寸压缩到指定大小
    :param infile: 压缩源文件
    :param outfile: 压缩文件保存地址
    :param mb: 压缩目标，KB
    :param step: 每次调整的压缩比率
    :param quality: 初始压缩比率
    :return: 压缩文件地址，压缩文件大小
    """
    o_size = get_size(infile)
    if o_size <= mb:
        return infile
    outfile=infile
    while o_size > mb:
        im = Image.open(infile)
        im.save(outfile, quality=quality)
        if quality - step < 0:
            break
        quality -= step
        o_size = get_size(outfile)
    return outfile, get_size(outfile)

def resize_image(infile, w,h):
    """修改图片尺寸
    :param infile: 图片源文件
    :param outfile: 重设尺寸文件保存地址
    :param w,h: 设置的宽、高
    :return:
    """
    im = Image.open(infile)
    out = im.resize((w, h), Image.ANTIALIAS)
    out.save(infile)
    
def change_format(infile,target='.jpg'):
    '''etc: source: '.png', target='.jpg'
    文件保存在原地
    '''
    img=Image.open(infile)
    outfile = os.path.splitext(infile)[0]+target
    try:
      if len(img.split())==4:
        r,g,b,a=img.split()
        img=Image.merge("RGB",(r,g,b))
        img.convert("RGB").save(outfile,quality=100)
        
      else:
        img.convert("RGB").save(outfile,quality=100)
        
    except Exception as e:
      print(e)    

count=1
total=str(len(img_path))
for infile in img_path:
    #修改文件格式
    target_format='.jpg'
    file_dir=os.path.splitext(infile)[0]
    print("("+str(count)+"/"+total+")process: ",infile)
    if os.path.splitext(infile)[1]!=target_format:
        change_format(infile,target='.jpg')
        os.remove(infile)
    infile=file_dir+target_format
    #resize_image(infile,512,512)
    compress_image(infile,mb=150)
    count+=1
