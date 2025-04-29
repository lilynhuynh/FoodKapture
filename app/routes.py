from flask import Blueprint, request, jsonify
from app.model.classify import run_inference
from app.utils.image_utils import preprocess_image

routes = Blueprint('routes', __name__)

@routes.route('/classify', methods=['POST'])
def classify():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    
    image = request.files['image']
    input_tensor = preprocess_image(image)
    output = run_inference(input_tensor)
    return jsonify({'result': output.tolist()})