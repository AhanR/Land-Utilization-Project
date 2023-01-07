import numpy as np
import glob
import cv2

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
                    # mapsValue.append((i-1)/len(marks) + (pixel[0] - marks[i-1][0])/len(marks)/(marks[i][0] - marks[i-1][0]))
    # totPixels = map.shape[0]*map.shape[1]
    if totpixels == 0:
        return -1
    totalScaleValue = totalScaleValue/totpixels*(scaleRange[1]-scaleRange[0]) + scaleRange[0]
    # print(min(mapsValue), max(mapsValue), map.shape[0]*map.shape[1] - totpixels)
    return (totalScaleValue)

mapValues = []
for mapPortion in glob.glob("Vandalur_NDVI//*.png"):
    mapPortionImage = cv2.imread(mapPortion, cv2.COLOR_BGR2HLS)
    mapValues.append(readMapScale(mapPortionImage, [lower_bound, middle_bound, upper_bound], [-0.3,0.63]))
print(mapValues)
mapValues = np.array(mapValues)
mapValues.tofile('Vandalur_NDVI_Data.csv', sep = ',')

# the solution that worked
# image = cv2.imread('Vandalur_NDVI//filename_209.png')
# image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
# print(readMapScale(image, [lower_bound,middle_bound,upper_bound],[-0.3,0.63]))