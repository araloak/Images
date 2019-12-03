from captcha.image import ImageCaptcha
import matplotlib.pyplot as plt
import numpy as np 
import random
import string
import sys
path=sys.path[0]
#characters为验证码上的字符集，10个数字加26个大写英文字母
#0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ str类型
def generate_captcha():
    characters=string.digits+string.ascii_uppercase

    width,height,n_len,n_class=100,100,4,len(characters)

    #设置验证码图片的宽度widht和高度height
    #除此之外还可以设置字体fonts和字体大小font_sizes
    generator=ImageCaptcha(width=width,height=height)

    #生成随机的4个字符的字符串
    random_str=''.join([random.choice(characters) for j in range(4)])

    #生成验证码
    img=generator.generate_image(random_str)

    #显示验证码图片和验证码标题
    '''
    plt.imshow(img)
    plt.title(random_str)
    plt.show()
    '''
    file_name=path+"\\captcha\\"+random_str+'.jpg'
    img.save(file_name)

if __name__== "__main__":
    for i in range(0,10):
        generate_captcha()
    #print("done")
