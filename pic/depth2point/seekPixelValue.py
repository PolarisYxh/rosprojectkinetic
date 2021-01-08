# 查找一个目录下所有图片（单通道）或单张图片（单通道）中出现过的像素值（0像素值不算）
import os
import glob
import shutil
import cv2
import numpy as np
from PIL import Image

# 查找一个目录下所有图片（单通道）出现过的像素值
def seekDirPixel(Path_to_Dataset):
    images = glob.glob(os.path.join(Path_to_Dataset, "*.png")) # images类型是list，每一个元素都存储的是图片的完整路径
    # images.sort()
    B = [] # 用来存像素值
    
    for img in images:
        b = seekFilePixel(img)
        B = list(set(B + b))
    print("本目录下一共出现过的像素值有(不算0像素)：", B)   
    
    
# 找一张单通道图片中出现过的像素值（0像素值不算）
def seekFilePixel(Path_to_Pic):
    image = cv2.imread(Path_to_Pic, cv2.IMREAD_UNCHANGED) # 不要第二个参数的话默认为3个通道
    # print("image的类型为：", type(image))
    # print(image)
    b = [] # 用来存像素值
    b.append(image[0][0])
    
    # 找像素值
    for i in range(image.shape[0]): # 行
        for j in range(image.shape[1]): # 列
            if image[i][j] not in b:
                b.append(image[i][j])
    if 0 in b:
        b.remove(0)
    print("正在处理的是：", Path_to_Pic)
    print("出现过的非零像素值有：", b)
    return b

def main():
    # seekDirPixel("C:/Users/jun/Desktop/depth")
    seekFilePixel("C:/Users/jun/Desktop/YXH_Indoor.png")
    
if __name__ == "__main__": 
    main()