import tensorflow as tf
import keras
import keras.backend as K
import os
import numpy as np
from PIL import Image
import sys


from keras.callbacks import LearningRateScheduler
if __name__ =='__main__':
    #脚本执行时自动将其路径添加到sys.path中
    train_path=sys.path[0]+'\\train\\'
    test_path=sys.path[0]+'\\test\\'
    result_path=sys.path[0]
    #numpy不能直接将高维list转化为numpy数组，所以要预先声明一个高维数组再改变每一条的值，而不能先将每个图片添加到临时列表中再array化列表
    #本次处理图片大小为50*50，3通道（RGB图像）
    train_data=np.zeros((64,50,50,3))
    test_data=np.zeros((2160,50,50,3))

    for i in range(0,64):
        filename=train_path+str(i)+'.png'
        train_data[i]= np.array(Image.open(filename))/255
    for i in range(1,2161):
        filename=test_path+str(i)+'.png'
        try:
            test_data[i]= np.array(Image.open(filename))/255
        except:
            print(i) 
    train_labels=[i for i in range(0,64)]
    #keras.utils.to_categorical函数根据传入的数组和规定的种类数量自动生成每个类别的onehot编码
    train_labels=keras.utils.to_categorical(train_labels,64)
    print('数据加载完成')

    drop_rate = 0.2
    num_nerons=1024 # 定义全连接层神经元个数

    def scheduler(epoch):#根据epoch调整学习率，epoch越大，学习率越小，防止震荡。
        if epoch % 100 == 0 and epoch != 0:
            lr = K.get_value(model.optimizer.lr)
            K.set_value(model.optimizer.lr, lr * 0.1)
            print("lr changed to {}".format(lr * 0.1))
        return K.get_value(model.optimizer.lr)


    model = keras.Sequential([
        #按顺序使用keras.layers中的类添加需要的层
        keras.layers.Conv2D(32,(5,5),padding='valid',activation='relu', input_shape=[50, 50, 3]), # Conv2D做第一层时需要额外提供参数input_shape(width,height,in_channels).keras内部会添加第四个参数（batch_size）
        keras.layers.Conv2D(64,(5,5),padding='valid',activation='relu'),
        keras.layers.MaxPool2D(pool_size=(2*2)),
        keras.layers.Flatten(),
        keras.layers.Dropout(drop_rate),
        keras.layers.Dense(num_nerons, activation='relu'),
        keras.layers.Dense(64, activation='softmax') ,  
    ])
    reduce_lr = LearningRateScheduler(scheduler)
    model.compile(optimizer='adam',
                  loss=keras.losses.categorical_crossentropy,#多分类时就使用keras自带categorical_crossentropy函数，否则可能会报错
                  metrics=['accuracy'])

    model.fit(train_data, train_labels, epochs=15, callbacks=[reduce_lr])
    model.save('model_1.h5')
    prediction=model.predict(test_data)
    result=[]
    for each in prediction:
        tem=list(each)
        #选择预测的最大值作为最终预测结果——其索引即可作为类别标签
        result.append(tem.index(max(tem)))
    #将结果保存在txt文档中，以‘，’为分隔，数据为整型
    np.savetxt(result_path+"//result.txt", result,fmt='%d',delimiter=',')
