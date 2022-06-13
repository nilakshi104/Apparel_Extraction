from PIL import Image
import os

directory="train"
c=0
for filename in os.listdir(directory):

    if filename.endswith(".jpg"):
        if c<100:
            im=Image.open(directory + '/' + filename)
            im=im.resize((512,512))
            rgb_img=im.convert('RGB')
            rgb_img.save(f'5classes/images_png/{c}.png')
            c+=1
            print(os.path.join(directory,filename))