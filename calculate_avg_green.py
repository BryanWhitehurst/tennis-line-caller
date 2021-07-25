import numpy as np
import cv2
import math

#Read in an image cropped down to the ball
#calculates average HSV values of image
def avgGreen(image):
    newImg = cv2.imread(image)
    newImg = cv2.cvtColor(newImg, cv2.COLOR_BGR2HSV)

    height = newImg.shape[0]
    width = newImg.shape[1]

    centerX = width / 2
    centerY = height / 2
    radius = width/ 2
    area = int(3.14 * radius * radius)
    hue = 0
    sat = 0
    val = 0
    total = 0

    for i in range(1, height):
        distFromCenter = abs(centerY  - i)
        length = int(math.sqrt(radius**2 - distFromCenter**2) * 2)
        cur = int(centerX - (length / 2))
        for j in range(cur, int(centerX + (length / 2))):
            h = newImg[i,j][0]
            s = newImg[i,j][1]
            v = newImg[i,j][2]
            if( not((h == 0 or h == 255) and (v == 0 or v == 255) and v == 255)): #ignore white
                hue = hue + h
                sat = sat + s
                val = val + v
                total = total + 1


    avgHue = hue / total
    avgSat = sat / total
    avgVal = val / total         

    return [avgHue, avgSat, avgVal]

 
