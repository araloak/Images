#该脚本用于剪裁大块空白的图片，只保留局部含有有效信息的区域，方便之后模型的学习
import numpy as np
import os
from PIL import Image
import sys

#在cut_image保存的目录下新建original_data文件夹保存原始训练图片；
#result文件夹保存切割后的图片

path=sys.path[0]+'\\original_data\\'
#图片以数字命名，方便加载

for flag in range(1,2161):
    filename=path+str(flag)+'.png'
    im = Image.open(filename)
    im_matrix=np.array(im)
    first=True
    for i,row in enumerate(im_matrix):
        for j,block in enumerate(row) :
            #检测到第一个非白色像素点,避免陷入死循环
            if block[0]!=255 and first==True:
                first=False
                #水平方向保留50个像素点
                new_im_matrix=im_matrix[i-10:i+40]
                image=[]
                for new_row in new_im_matrix:
                    rows=[]
                    for x,new_block in enumerate(new_row):
                        #竖直方向保留50个像素点
                        if x>=j-20 and x<=j+29:
                            rows.append(list(new_block))
                    image.append(rows)                    
                new_im_matrix=np.array(image)
                print(new_im_matrix.shape)
                #输出剪裁后图像的大小（此处为(50,50,3)）
                new_im = Image.fromarray(new_im_matrix)  
                new_im.save(sys.path[0]+"\\result\\"+str(flag)+'.png','PNG')
                print(flag)
        
