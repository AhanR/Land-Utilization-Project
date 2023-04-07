import os
import glob

def rename(folder = "Vandalur_LST"):
    mapSegments = glob.glob(folder+"/*.png")
    print("found "+str(len(mapSegments))+" images to rename")
    for file in mapSegments:
        imnum = (int(file.split("\\")[-1].split("-")[1])-1)*20 + (int(file.split("\\")[-1].split("-")[3][:-4])-1)
        newname = "\\".join(file.split("\\")[:-1])+ "\\" + format(imnum,'04d') + ".png"
        # print(newname)
        os.rename(file, newname)
    print("renaming complete")

rename("Vandalur_NDVI")