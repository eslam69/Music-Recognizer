
import numpy as np
import os
from PIL import Image
import imagehash


number = 0
for filename in os.listdir():   ###### you have to be in the folder of spectogram images
    if filename.endswith(".png"):


        hashcode = imagehash.phash(Image.open(filename) )
        print(int(str(hashcode),16))
        f = open('hashes/'+os.path.splitext(os.path.basename(filename))[0]+'.txt','w')
        f.write(str(hashcode))
        f.close()
        number +=1
print(number)