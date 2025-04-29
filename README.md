# FoodKapture

## File Structure

FoodKapture/
│
├── app/
│   ├── __init__.py
│   ├── routes.py # Flask routes (API endpoints)
│   ├── model/ # Model loading and inference logic
│   │   ├── __init__.py
│   │   └── classify.py
│   └── utils/ # Preprocessing, postprocessing
│       └── image_utils.py
│
├── static/ # Static files (JS, CSS, etc.)
├── templates/ # HTML templates (if using Flask for rendering)
│
├── model/ # Saved model files (e.g., .pt, .h5)
│   └── unet_model.pt
│
├── uploads/ # Uploaded images (optional)
│
├── run.py # Entry point to run the Flask app
├── requirements.txt # Python dependencies
└── README.md

## Dependencies

Set up dependencies with installing all requirements with
`pip install -r requirements.txt`