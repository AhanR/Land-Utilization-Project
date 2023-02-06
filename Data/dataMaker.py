import numpy as np
import glob
import cv2
import sys
import os

# "#ffff00"
# np.array([255,255,0])
middle_bound = np.array([30, 255, 255])
# "#006100"
# np.array([0, 97, 0])
upper_bound = np.array([60, 255, 48])
# "#ff2600"
# np.array([255, 38, 0])
lower_bound = np.array([4, 255, 255])

# Take HSL value map reading in numpy
def readMapScale(map, marks, scaleRange):
    totalScaleValue = 0
    # mapsValue = []
    totpixels = 0
    for pixelRow in map:
        for pixel in pixelRow:
            for i in range(1,len(marks)):
                if pixel[0] <= marks[i][0] and pixel[0] > marks[i-1][0]:
                    totpixels += 1
                    totalScaleValue += (i-1)/len(marks) + (pixel[0] - marks[i-1][0])/len(marks)/(marks[i][0] - marks[i-1][0])
    if totpixels == 0:
        return None
    totalScaleValue = totalScaleValue/totpixels*(scaleRange[1]-scaleRange[0]) + scaleRange[0]
    return (totalScaleValue)

def readMapMapped(map, colourMap):
    features = []
    for pixelRow in map:
        for pixel in pixelRow:
            p = hsvToStr(pixel)
            if p in colourMap.keys() and colourMap[p] not in features:
                features.append(colourMap[p])
    return features

def strToHsv(s):
    ans = []
    for n in s[1:-1].split(","):
        if len(n) > 0:
            ans.append(int(n))
    return np.array(ans)

def hsvToStr(arr):
    return "["+str(arr[0]) + "," + str(arr[1]) + "," + str(arr[2]) + "]"

# Colour Print ---------------------------------------------------------------------------------------------
def prRed(skk): print("\033[91m {}\033[00m" .format(skk))
 
 
def prGreen(skk): print("\033[92m{}\033[00m" .format(skk))
 
 
def prYellow(skk): print("\033[93m{}\033[00m" .format(skk))
 
 
def prLightPurple(skk): print("\033[94m{}\033[00m" .format(skk))
 
 
def prPurple(skk): print("\033[95m{}\033[00m" .format(skk))
 
 
def prCyan(skk): print("\033[96m{}\033[00m" .format(skk))
 
 
def prLightGray(skk): print("\033[97m{}\033[00m" .format(skk))
 
 
def prBlack(skk): print("\033[98m{}\033[00m" .format(skk))

# Main program ----------------------------------------------------------------------------------------------

if len(sys.argv) < 2:
    print("invalid args")
    exit()
else:
    folderName = sys.argv[1]
    mapType = sys.argv[2]
    mapValues = []
    if mapType == "linear":
        mapRange = [strToHsv(x) for x in sys.argv[3:]]
        prLightPurple("Evaluating the map...")
        mapsSegments = glob.glob(folderName+"/*.png")
        prYellow("found " + str(len(mapsSegments))+" images in folder to evaluate")
        for mapPortion in mapsSegments:
            mapPortionImage = cv2.imread(mapPortion, cv2.COLOR_BGR2HLS)
            mapValues.append(readMapScale(mapPortionImage, mapRange, [x/(len(mapRange)) for x in range(1,len(mapRange)+1)]))
        prGreen(folderName+" Map Evaluated, data saved in : " + folderName + "_Data.csv")
        mapValues = np.array(mapValues)
        mapValues.tofile(folderName+'_Data.csv', sep = ',')
    elif mapType == "mapped":
        colourMap = dict((subString.split(":")[1],subString.split(":")[0]) for subString in sys.argv[3].split(";"))
        # print(colourMap)
        prLightPurple("Beginning map processing..")
        print(folderName+"/*.png")
        mapsSegments = glob.glob(folderName+"/*.png")
        prYellow("found " + str(len(mapsSegments))+" images in folder to evaluate")
        for mapPortion in mapsSegments:
            mapPortionImage = cv2.imread(mapPortion, cv2.COLOR_BGR2HLS)
            values = readMapMapped(mapPortionImage, colourMap)
            s = ""
            for t in values:
                s+=t+" "
            mapValues.append(s)
        prGreen(folderName+" Map evaluated for mapping, data saved in : " + folderName + "_Data.csv")
        # print(mapValues)
        np.array(mapValues).tofile(folderName+"_Data.csv", sep=",")
    else:
        prRed("invalid selection")
        exit()
    prLightGray("Operation Complete")
    exit()

# the solution that worked
# image = cv2.imread('Vandalur_NDVI//filename_209.png')
# image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
# print(readMapScale(image, [lower_bound,middle_bound,upper_bound],[-0.3,0.63]))