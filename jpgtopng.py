from PIL import Image
import os

def jpgtopng(inputDir):
    fileList = os.listdir(inputDir)
    for fileName in fileList:
        if len(fileName) > 20:
            fileDir = os.path.join(inputDir, fileName)
            im = Image.open(fileDir)
            im.save("/home/wanyi/mve/Data/InputImage/" + fileName[:-4] + ".png")


jpgtopng("/media/wanyi/SSD1/GzUniv/GZImages")

