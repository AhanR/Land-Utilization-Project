import os
import glob

def rename(folder = "Vandalur_LST"):
    mapSegments = glob.glob(folder+"/*.png")
    print("found "+str(len(mapSegments))+" images to rename")
    for file in mapSegments:
        newname = "\\".join(file.split("\\")[:-1])+ "\\" +format(int(file.split("\\")[-1][:-4]),'04d') + ".png"
        print(newname)
        os.rename(file, newname)

rename()