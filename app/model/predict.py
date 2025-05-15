"""
File: predict.py
Description: Placeholder model that calls a yolov5 model to get the detected
items from the given image and returns the detected class names
"""
import torch
from torchvision import transforms
from PIL import Image, ImageOps
import numpy as np
from ultralytics import YOLO
import time
import sys

# Set device
device = 'cpu'
if torch.cuda.is_available():
    device = 'cuda'

# Load model
start = time.time()
model = YOLO('model/yolov5su.pt')
print(f"Model loaded in {time.time() - start:.2f} seconds")


def run_inference(input_tensor):
    """
    Given a processed image, it will detect the images and return the detected
    image labels
    """
    print("==>Running model inference...")
    results = model(input_tensor)
    predicted_classes = []

    predictions = results[0].boxes
    classes = predictions.cls

    for class_id in classes:
        class_id = int(class_id.item())
        class_name = results[0].names[class_id]
        print(class_name)
        predicted_classes.append(class_name)

    print("==> In predict.py, expected result:", predicted_classes)

    return predicted_classes