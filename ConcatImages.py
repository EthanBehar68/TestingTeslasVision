from PIL import Image
import cv2
import os

def get_concat_h(imageList):
    largestHeight = 0
    totalWidth = 0
    for image in imageList:
        totalWidth += image.width
        if image.height > largestHeight:
            largestHeight = image.height

    dst = Image.new('RGB', (totalWidth, largestHeight))

    previousWidth = 0
    for image in imageList:
        dst.paste(image, (previousWidth, 0))
        previousWidth += image.width
    
    return dst


ogImages = [image for image in os.listdir("D:\Projects\TestingTeslasVision\AE DAG - Take 3\og")]
ogImages.sort()

for i in range(len(ogImages)):
    basename = os.path.basename(ogImages[i]).replace('.png', '')
    print(basename)


    ogImage = Image.open("D:\Projects\TestingTeslasVision\AE DAG - Take 3\og\\" + ogImages[i])
    ogPrediction = Image.open("D:\Projects\TestingTeslasVision\AE DAG - Take 3\og_predictions\\" + basename + "_predictions.png")
    perturbImage = Image.open("D:\Projects\TestingTeslasVision\AE DAG - Take 3\perturbed\\" + basename + "_perturbation.png")
    advImage = Image.open("D:\Projects\TestingTeslasVision\AE DAG - Take 3\\adv\\" + ogImages[i])
    advPredictionsImage = Image.open("D:\Projects\TestingTeslasVision\AE DAG - Take 3\\adv_predictions\\" + basename + "_adv_predictions.png")

    get_concat_h([ogImage, ogPrediction, perturbImage, advImage, advPredictionsImage]).save("D:\Projects\TestingTeslasVision\AE DAG - Take 3\concats\\" + str(i) + ".png")
