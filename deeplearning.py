import numpy as np
import cv2
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import pytesseract as pt
from PIL import Image, ImageFilter
from ultralytics import YOLO
from roboflow import Roboflow
from flask_cors import CORS

rf = Roboflow(api_key="Bv81WfXp2nY9ZIi2UdH6")
project = rf.workspace().project("vehicle-registartion-plate-finder")

modelRf = project.version(2).model
modelYolov8 = YOLO('./static/models/yolov8v2.pt')
modelInceptionResnetv2 = tf.keras.models.load_model('./static/models/object_detection_decay.h5')







def modify(path, filename):
    results = modelYolov8(path)
    cods = results[0].boxes.xyxy
    img = np.array(Image.open(path))
    
    image = Image.open(path)
    image.load()
    
    for cord in cods:
        xmin, ymin,xmax,  ymax = map(int, cord)  # Convert Tensor values to integers
        
        crop = image.crop((xmin, ymin, xmax, ymax))
        image.paste(crop.filter(ImageFilter.GaussianBlur(20)), (xmin, ymin))
  
        roi = img[ymin:ymax, xmin:xmax]
        roi_bgr = cv2.cvtColor(roi, cv2.COLOR_RGB2BGR)
        # cv2.imwrite('./static/roi/{}'.format(filename), roi_bgr)
    image = image.save('./static/modified_uploads/{}'.format(filename))
    text="abc"
    #text = pt.image_to_string(roi)
    #print(text)
    return text


