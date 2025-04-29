import torch
from torchvision import transforms
from PIL import Image

# Load model
device = 'cpu'

if torch.cuda.is_available():
    device = 'cuda'

model = torch.load('model/...', map_location=device)
model.eval()

def run_inference(input_tensor):
    with torch.no_grad():
        output = model(input_tensor.unsqueeze(0))
    return output.squeeze(0)