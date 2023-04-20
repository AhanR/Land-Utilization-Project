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
    totpixels = 0
    pixelValue = 0
    # calculate the average hue for all colours except white and black
    # when saturation value is zero, the colour is between black and white so checking for satuation value zero (pixel[2]) is good enough for right now
    for pixelRow in map:
        for pixel in pixelRow:
            if type(pixel) == type(np.array([])) and pixel[2]!=0 and pixel[0] != 255:
                pixelValue += pixel[0]
                totpixels+=1
    # totpixels = len(mapsValue)
    if totpixels == 0:
        return None
    avgPixel = pixelValue/totpixels
    for i in range(1,len(marks)):
        if type(avgPixel) != type(np.array([])):
            if avgPixel <= marks[i][0] and avgPixel > marks[i-1][0]:
                totpixels += 1
                totalScaleValue += (i)/len(marks) + (avgPixel - marks[i-1][0])/len(marks)/(marks[i][0] - marks[i-1][0])
                break
        else:
            if avgPixel[0] <= marks[i][0] and avgPixel[0] >= marks[i-1][0]:
                totpixels += 1
                totalScaleValue += (i)/len(marks) + (avgPixel[0] - marks[i-1][0])/len(marks)/(marks[i][0] - marks[i-1][0])
                break
    totalScaleValue = totalScaleValue*(scaleRange[1]-scaleRange[0]) + scaleRange[0]
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
    return "[" + str(arr[0]) + "," + str(arr[1]) + "," + str(arr[2]) + "]"

def printHelp():
    prGreen("Use the following options:")
    prLightPurple("python dataMaker.py <MAP NAME> <MAP TYPE> <EXTRA ARGUMENTS>")
    prYellow("MAP TYPES:")
    prLightGray("linear, mapped")
    prYellow("EXTRA ARGUMENTS")
    prLightGray("Can be colour values in array or map values as a JSON")

# Colour Print ---------------------------------------------------------------------------------------------
def prRed(skk): print("\033[91m{}\033[00m" .format(skk))

def prGreen(skk): print("\033[92m{}\033[00m" .format(skk))

def prYellow(skk): print("\033[93m{}\033[00m" .format(skk))

def prLightPurple(skk): print("\033[94m{}\033[00m" .format(skk))

def prPurple(skk): print("\033[95m{}\033[00m" .format(skk))

def prCyan(skk): print("\033[96m{}\033[00m" .format(skk))

def prLightGray(skk): print("\033[97m{}\033[00m" .format(skk))

def prBlack(skk): print("\033[98m{}\033[00m" .format(skk))

# Main program ----------------------------------------------------------------------------------------------
if sys.argv[1] == "help":
    printHelp()
elif len(sys.argv) < 2:
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
        # prYellow("found " + str(len(mapsSegments))+" images in folder to evaluate")
        prYellow("Colour Domain: "+str(mapRange))
        for mapPortion in mapsSegments:
            mapPortionImage = cv2.imread(mapPortion)
            mapPortionImage = cv2.cvtColor(mapPortionImage, cv2.COLOR_BGR2HSV)
            mapValues.append(readMapScale(mapPortionImage, mapRange,[0] + [1]))
        prGreen(folderName+" Map Evaluated, data saved in : " + folderName + "_Data.csv")
        mapValues = np.array(mapValues)
        filteredValues = [x for x in filter(lambda x:x!=None,mapValues)]
        prLightGray("Maximum: "+str(max(filteredValues)))
        prLightGray("Minimum: "+str(min(filteredValues)))
        prLightGray("Average: "+str(sum(filteredValues)/len(mapValues)))
        prLightGray("Non empty items: "+str(len(filteredValues))+"/"+str(len(mapsSegments)))
        prLightGray("Variance: "+str(np.var(filteredValues)))
        mapValues.tofile("Data Generated/"+folderName+"_Data.csv", sep=",")
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
        prGreen(folderName+" Map evaluated for mapping, data saved in : ./Data Generated" + folderName + "_Data.csv")
        # print(mapValues)
        # This is where the change was made for the file reading the data mirrored across the origin
        np.array(mapValues[::-1]).tofile("Data Generated/"+folderName+"_Data.csv", sep=",")
    else:
        prRed("invalid selection")
        exit()
    prGreen("Operation Complete")
    exit()

# the solution that worked
# image = cv2.imread('Vandalur_NDVI//filename_209.png')
# image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
# print(readMapScale(image, [lower_bound,middle_bound,upper_bound],[-0.3,0.63]))
# ub [0,128,211]
# mb [60,176,240]
# lb [200,255,255]