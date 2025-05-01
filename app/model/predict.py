import torch
from torchvision import transforms
from PIL import Image, ImageOps
import numpy as np
from ultralytics import YOLO
import time

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
    results = model(input_tensor)
    return results[0].boxes.data.tolist()

# transform = transforms.Compose([
#     transforms.Resize((128, 128)), # TODO - based on model input size
#     transforms.ToTensor(),
# ])

# def run_inference(input_tensor):
#     with torch.no_grad():
#         output = model(transform(input_tensor).unsqueeze(0))
#     return output.squeeze(0).numpy().tolist()