import pandas as pd
import cv2
import numpy as np
import json
import matplotlib.pyplot as plt

df = pd.read_csv('train.csv')
df['CategoryId'] = df['ClassId'].str.split('_').str[0]
# print(df)

with open("label_descriptions.json") as f:
    label_descriptions = json.load(f)   
# print(label_descriptions)

IMAGE_SIZE=512
def show_img(img,img_name):
    # imaterialist-fashion-2019-FGVC6/ dataset
    I = cv2.imread("train/" + img, cv2.IMREAD_COLOR)
    I = cv2.cvtColor(I, cv2.COLOR_BGR2RGB)
    I = cv2.resize(I, (IMAGE_SIZE, IMAGE_SIZE), interpolation=cv2.INTER_AREA) 
    cv2.imwrite(f'E:/cloths_segmentation/5classes/images_png/whole_new/{img_name}.png',I)
    
    return I
    
ids = df['ImageId'].unique()
# ids[0]
# img=show_img(ids[0],0)


dict1={0:[26,25,24,23,22,18,15,14,13],
     1:[27,9,5,4,3,2,1,0, 33, 43, 31, 30, 29, 28, 16, 17],
     2:[12,11,10, 32, 36, 37, 38, 39, 40, 44],
     3:[21, 8, 7, 6, 34, 35, 42, 45, 41, 20, 19]
    }
    #  4:[45,44,43,42,41,40,39,38,37,36,35,34,33,32,31,30,29,28,20,19,17,16]}

count=0
with open('5classes\img_id_name.txt','w') as f:
    for img_id in ids[1:10000]:
        f.write(str(img_id))
        f.write('\n')
        count+=1
        input_img=show_img(img_id,str(count))
        a = df[df.ImageId == img_id]
        a = a.groupby('CategoryId',as_index=False).agg({'EncodedPixels':' '.join, 'Height':'first','Width':'first'})  
        H = a.iloc[0,2]
        W = a.iloc[0,3]
        masked_list=[]
        categories=[]
        for line in a[['EncodedPixels','CategoryId']].iterrows():
            for key,val in dict1.items():
                if int(line[1][1]) in val:
                    updated_line_11=key

            mask=np.full(H*W,dtype='int32',fill_value=0)
            EncodedPixels = line[1][0]
            pixel_loc = list(map(int,EncodedPixels.split(' ')[0::2]))
            iter_num =  list(map(int,EncodedPixels.split(' ')[1::2]))
            for p,i in zip(pixel_loc,iter_num):
                mask[p:(p+i)] = updated_line_11
            mask = mask.reshape(W,H).T
            # plt.figure()
            # plt.imshow(mask)
            masked_list+=[mask]
            categories+=[updated_line_11]
            
        # plt.figure(figsize=[30,30])
        # plt.subplot(1,2,1)
        # plt.imshow(input_img) 
        # plt.title('Input Image') 
        
        matrix = np.zeros((IMAGE_SIZE,IMAGE_SIZE),dtype='int32')
        for i in range(0, len(masked_list)):
            masked_list[i] = cv2.resize(masked_list[i], (IMAGE_SIZE,IMAGE_SIZE), interpolation=cv2.INTER_NEAREST)
        for m in masked_list:
            for i in range(0, IMAGE_SIZE):
                for j in range(0,IMAGE_SIZE):
                    if m[i][j] != 0:
                        # matrix[i][j]=m[i][j]* 63
                        matrix[i][j]=m[i][j]
                        # print(m[i][j]* 63)
        # # matrix = np.array(matrix,dtype='uint8')
        # print(np.unique(matrix))
        # print(matrix.shape)
        # print(matrix.dtype)
        # plt.subplot(1,2,2)
        # plt.imshow(matrix)  
        # plt.title('Mask')
        # plt.show()
        cv2.imwrite(f'E:/cloths_segmentation/5classes/masks1_png/whole_new/{count}.png',matrix)