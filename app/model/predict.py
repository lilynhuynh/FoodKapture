import torch
from torchvision import transforms
from PIL import Image, ImageOps
import numpy as np
from ultralytics import YOLO
import time
import sys

# Load model
device = 'cpu'

if torch.cuda.is_available():
    device = 'cuda'

start = time.time()
model = YOLO('model/yolov5su.pt')
print(f"Model loaded in {time.time() - start:.2f} seconds")

# model = torch.hub.load('model/ultralytics/yolov5', 'yolov5s', pretrained=True, map_location=device)
# model.eval()

def run_inference(input_tensor):
    print("==>Running model inference...")
    results = model(input_tensor)
    # print("==>Model returned", results)

    # print(results[0].boxes.cls.tolist())
    # print("==> Boxes accessed")

    # Get prediction
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

# transform = transforms.Compose([
#     transforms.Resize((128, 128)), # TODO - based on model input size
#     transforms.ToTensor(),
# ])

# def run_inference(input_tensor):
#     with torch.no_grad():
#         output = model(transform(input_tensor).unsqueeze(0))
#     return output.squeeze(0).numpy().tolist()