from flask import Blueprint, request, jsonify, render_template
from app.model.predict import run_inference
from app.utils.image_utils import preprocess_image
import os
from datetime import datetime

routes = Blueprint('routes', __name__)

@routes.route("/", methods=["GET"])
def home():
    print("==> Loaded home route")
    return render_template("index.html")

UPLOAD_FOLDER_PATH = os.path.join(os.path.dirname(__file__), "..", "uploads")
os.makedirs(UPLOAD_FOLDER_PATH, exist_ok=True)

@routes.route('/classify', methods=['POST'])
def classify():
    print("==> In classify in routes.py")
    if 'image' not in request.files:
        print("==> No image part in request")

        return jsonify({'error': 'No image uploaded'}), 400
    
    image = request.files['image']
    print(f"==> Got file {image.filename}")

    processed_img = preprocess_image(image)

    # if image.filename == '':
    #     print(f"==> No selected file")
    #     return jsonify({"error": "No file selected"}, 400)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"upload_{timestamp}.jpg"
    savePath = os.path.join(UPLOAD_FOLDER_PATH, filename)
    processed_img.save(savePath, format="JPEG")
    print("==> File saved successfully")

    output = run_inference(processed_img)
    return jsonify({'result': output})
    # return jsonify({'message': 'Image Saved!', 'filename': filename}, 200)