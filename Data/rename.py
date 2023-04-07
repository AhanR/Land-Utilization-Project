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

# def recount(folder="Vandalur_LST"):
#     mapSegments = glob.glob(folder+"/*.png")
#     print("Found "+str(len(mapSegments)) + " images")
#     for i in range(1,len(mapSegments)+1):
#         if format(i, '04d') + ".png" in 

rename("Vandalur_NDVI")