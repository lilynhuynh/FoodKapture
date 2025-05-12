import os
import pyheif
from PIL import Image

def preprocess_image(image_file):
    filename = image_file.filename.lower()

    # Handling HEIC file types
    if filename.endswith(".heic"):
        heif_img = pyheif.read(image_file.read())
        image = Image.frombytes(
            heif_img.mode,
            heif_img.size,
            heif_img.data,
            "raw",
        )
    else:
        image = Image.open(image_file)

    # Handling JPEG - return as-is
    return image.convert("RGB")
