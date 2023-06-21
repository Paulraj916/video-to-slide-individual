import os
import glob
import cv2
import time
from pptx1 import pptx1

pptx1 = pptx1("image")
class img2s:
    def __init__(self,make):
        self.make = make
        start_time = time.time() 
        for img in glob.glob("images/*.png"):
            path= os.path.join(img)
            img1 = cv2.imread(path)
            img2 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
            pptx1.convert_screenshots_to_pptx(img2,path) 
        for img in glob.glob("images/*.jpg"):
            path= os.path.join(img)
            img1 = cv2.imread(path)
            img2 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
            pptx1.convert_screenshots_to_pptx(img2,path) 
        for img in glob.glob("images/*.jpeg"):
            path= os.path.join(img)
            img1 = cv2.imread(path)
            img2 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
            pptx1.convert_screenshots_to_pptx(img2,path) 
        print(f'Time taken {time.time()-start_time}s') 