# -*- coding: utf-8 -*-
"""B546 Project: Model Training.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1FalDA23baaEK-ue8qCXgIbDaWtMnmOvg

# **B546 Final Project: Testing Tesla's Vision**
# **Using Detectron 2, COCO Data Format, And Instance Segmentation**

<img src="https://dl.fbaipublicfiles.com/detectron2/Detectron2-Logo-Horz.png" width="100"> https://github.com/facebookresearch/detectron2
COCO https://cocodataset.org/#home

NOTE: This notebook includes only what's necessary to run in Colab.
--------------------------------------------------------------------------------
I built everything using the tools, resources, and guides.

Webcrawler to download images: 

https://github.com/amineHorseman/images-web-crawler/

Labelme to annotate images: 

https://github.com/wkentaro/labelme

Convert Labelme to COCO dataset:

https://github.com/Tony607/labelme2coco/blob/master/labelme2coco.py

Comprehensive Guides:

https://www.dlology.com/blog/how-to-create-custom-coco-data-set-for-instance-segmentation/

https://www.dlology.com/blog/how-to-train-detectron2-with-custom-coco-datasets/

Adversarial Example:

https://github.com/lemonwaffle/detectron2-1
"""

print("Don't timeout please")

"""## Install Detectron2 And Necessary Dependencies


"""

# Install dependencies: 
!pip install pyyaml==5.1 pycocotools>=2.0.1

# Install Detectron2
!pip install detectron2 -f https://dl.fbaipublicfiles.com/detectron2/wheels/cu101/torch1.6/index.html
import torch, torchvision

"""## Prepare Model Training Dataset And COCO Data"""

# Download our dataset (images of bicycles) and COCO data as a json file.
# Note I found downloading very inconsistent. I'm not sure if that's b/c my git went over its size limit.
# So I resorted to manually uploading the files I need.

# !wget https://github.com/EthanBehar68/TestingTeslasVision/blob/main/BicycleImagesTrainingSet.zip?raw=true
# !mv BicycleImagesTrainingSet.zip?raw=true BicycleImagesTrainingSet.zip
# !wget https://raw.githubusercontent.com/EthanBehar68/TestingTeslasVision/main/BicycleTrainingSetCOCOData.json

!unzip TrainingSet.zip
# !unzip TrainingSet_Adv.zip
# !unzip sample.zip

"""## Register Model Dataset With Detectron2"""

# Import Detectron2 and set up logger
import detectron2
from detectron2.utils.logger import setup_logger
setup_logger()

# Import some common libraries
import numpy as np
import cv2
import matplotlib.pyplot as plt
import os
import random

# Import some common detectron2 utilities
from detectron2 import model_zoo
from detectron2.config import get_cfg
from detectron2.data import MetadataCatalog
from detectron2.engine import DefaultTrainer
from detectron2.engine import DefaultPredictor
from detectron2.utils.visualizer import Visualizer
from detectron2.utils.visualizer import ColorMode
#import the COCO Evaluator to use the COCO Metrics
from detectron2.evaluation import COCOEvaluator, inference_on_dataset
from detectron2.data import build_detection_test_loader

# Register our COCO json file
from detectron2.data.datasets import register_coco_instances
register_coco_instances("model_train", {}, "./TrainingSetCOCOData.json", "./TrainingSet/")
register_coco_instances("model_train_adv", {}, "./TrainingSetCOCOData.json", "./TrainingSet_Adv/")


from detectron2.data import DatasetCatalog, MetadataCatalog
modelDataDicts = DatasetCatalog.get("model_train")
modelMetaData = MetadataCatalog.get("model_train")

# This is solely for the purpose of verfying the COCO json file works properly.
# This step is not necessary for training.

# for data in modelDataDicts: # View all of the images/data
for data in random.sample(modelDataDicts, 3): # sample of 3
    print(data["file_name"])
    image = cv2.imread(data["file_name"])
    visualizer = Visualizer(image[:, :, ::-1], metadata=modelMetaData, scale=0.5)
    visualizer = visualizer.draw_dataset_dict(data)
    plt.figure(figsize = (14, 10))
    plt.imshow(cv2.cvtColor(visualizer.get_image()[:, :, ::-1], cv2.COLOR_BGR2RGB))
    plt.show()

"""## Train Model Without A .pth File

NOTE: This step can take longer than an hour. BE SURE THE COLAB NOTEBOOK DOES NOT TIMEOUT/DISCONNECT!!! KEEP IT IN FOCUS!
"""

cfg = get_cfg()
cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
cfg.DATASETS.TRAIN = ("model_train",)
cfg.DATASETS.TEST = ()
cfg.DATALOADER.NUM_WORKERS = 2
cfg.MODEL.WEIGHTS = "" # This is empty b/c we are training a brand new model.
cfg.SOLVER.IMS_PER_BATCH = 2
cfg.SOLVER.BASE_LR = 0.001
cfg.SOLVER.MAX_ITER = 100000
cfg.MODEL.ROI_HEADS.NUM_CLASSES = 2

os.makedirs(cfg.OUTPUT_DIR, exist_ok=True)
trainer = DefaultTrainer(cfg) 
trainer.resume_or_load(resume=False)
trainer.train()

# Don't forget to download the model!

"""## Use Trained Model For Inference"""

cfg = get_cfg()
cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
cfg.DATASETS.TRAIN = ("model_train",)
cfg.DATASETS.TEST = ("model_eval", )
cfg.DATALOADER.NUM_WORKERS = 2
cfg.MODEL.WEIGHTS = "./output/model_final.pth"
cfg.SOLVER.IMS_PER_BATCH = 2
cfg.SOLVER.BASE_LR = 0.001
cfg.SOLVER.MAX_ITER = 10000
cfg.MODEL.ROI_HEADS.NUM_CLASSES = 2
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5 
cfg.TEST.EVAL_PERIOD = 500 # No. of iterations after which the Validation Set is evaluated. 

# Create Predictor And Trainer
trainer = DefaultTrainer(cfg) 
trainer.resume_or_load(resume=True)
predictor = DefaultPredictor(cfg)

# Single predict on one specific image
image = cv2.imread('./1.png')
outputs = predictor(image)
visualizer = Visualizer(image[:, :, ::-1],
                metadata=modelMetaData, 
                scale=0.8, 
                instance_mode=ColorMode.IMAGE_BW   # remove the colors of unsegmented pixels
)
visualizer = visualizer.draw_instance_predictions(outputs["instances"].to("cpu"))
plt.figure(figsize = (14, 10))
plt.imshow(cv2.cvtColor(visualizer.get_image()[:, :, ::-1], cv2.COLOR_BGR2RGB))
plt.show()

# Iterate over images and predict on image.
directory = './TrainingSet/'

images = [image for image in os.listdir(directory) if image.endswith('.png')]

for fileName in images:    
    print(directory + fileName)
    image = cv2.imread(directory + fileName)
    outputs = predictor(image)
    visualizer = Visualizer(image[:, :, ::-1],
                   metadata=modelMetaData, 
                   scale=0.8, 
                   instance_mode=ColorMode.IMAGE_BW   # remove the colors of unsegmented pixels
    )
    visualizer = visualizer.draw_instance_predictions(outputs["instances"].to("cpu"))
    plt.figure(figsize = (14, 10))
    plt.imshow(cv2.cvtColor(visualizer.get_image()[:, :, ::-1], cv2.COLOR_BGR2RGB))
    plt.show()

# Iterate over AE and original images and predict.
directory = './TrainingSet_Adv/'

images = [image for image in os.listdir(directory) if image.endswith('.jpg')]
images.sort()

for fileName in images:    
    print(directory + fileName)
    image = cv2.imread(directory + fileName)
    outputs = predictor(image)
    visualizer = Visualizer(image[:, :, ::-1],
                   metadata=modelMetaData, 
                   scale=0.8, 
                   instance_mode=ColorMode.IMAGE_BW   # remove the colors of unsegmented pixels
    )
    visualizer = visualizer.draw_instance_predictions(outputs["instances"].to("cpu"))
    plt.figure(figsize = (14, 10))
    plt.imshow(cv2.cvtColor(visualizer.get_image()[:, :, ::-1], cv2.COLOR_BGR2RGB))
    plt.show()

"""## Evaluation Of The Trained Model (used for testing against training data ground truth)"""

# This is the normal dataset results
# Call the COCO Evaluator function and pass the Validation Dataset
evaluator = COCOEvaluator("model_train", cfg, False, output_dir="/output/")
val_loader = build_detection_test_loader(cfg, "model_train")

# Use the created predicted model in the previous step
inference_on_dataset(predictor.model, val_loader, evaluator)

# This is the adversarial example dataset results
# Call the COCO Evaluator function and pass the Validation Dataset
evaluator = COCOEvaluator("model_train", cfg, False, output_dir="/output/")
val_loader = build_detection_test_loader(cfg, "model_train_adv")

# Use the created predicted model in the previous step
inference_on_dataset(predictor.model, val_loader, evaluator)