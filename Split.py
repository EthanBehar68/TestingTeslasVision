from PIL import Image
import cv2
import os

image = Image.open("D:\Projects\TestingTeslasVision\Control\BicycleWithPersonGS9-print.png")

cut = 8

splitWidth = image.width//cut
splitHeight = image.height//cut
left = 0
upper = 0
right = splitWidth
lower = splitHeight

x = 0
for i in range(cut):
    for j in range(cut):
        print(left)
        print(upper)
        print(right)
        print(lower)
        Image.open("D:\Projects\TestingTeslasVision\Control\BicycleWithPersonGS9-print.png").crop((left, upper, right, lower)).save("D:\Projects\TestingTeslasVision\AE DAG - Take 3\splits\\11in_" + str(x) + ".png")
        left += splitWidth
        right += splitWidth
        x += 1
    upper += splitHeight
    lower += splitWidth
    left = 0
    right = splitWidth
