# from flask import Blueprint, request, jsonify, render_template
# from app.model.predict import run_inference
# from app.utils.image_utils import preprocess_image
# import os
# from datetime import datetime

from fastapi import APIRouter, Request, UploadFile, File, HTTPException, Form
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
import os
from .utils.image_utils import preprocess_image
from .model.predict import run_inference
from .utils.log_entries import create_new_meal_entry
import sqlite3
import json
from datetime import datetime

router = APIRouter()

BASE_DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIRECTORY = os.path.join(BASE_DIRECTORY, 'templates')
print("TEMPLATES_PATH =", os.path.abspath(TEMPLATES_DIRECTORY))
templates = Jinja2Templates(directory=TEMPLATES_DIRECTORY)

UPLOAD_FOLDER_PATH = os.path.join(os.path.dirname(__file__), "..", "uploads")
os.makedirs(UPLOAD_FOLDER_PATH, exist_ok=True)

# Connect to database (create if does not exist)
connect = sqlite3.connect("foodKapture.db")
cursor = connect.cursor()

# cursor.execute("""
#     ALTER TABLE loggedEntriesCount
#     ADD totalCarbs NUMBER;
# """)
# connect.commit()

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    print("==> Rendering index.html")  # Add this
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    return templates.TemplateResponse("index.html",
    {"request": request, "timestamp": timestamp})

@router.get("/render_scan_page", response_class=HTMLResponse)
async def scan(request: Request):
    print("==> Rendering scan.html")  # Add this
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    return templates.TemplateResponse("scan.html",
    {"request": request, "timestamp": timestamp})

@router.get("/render_detected_page", response_class=HTMLResponse)
async def detect(request: Request):
    print("==> Rendering detected.html")  # Add this
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    return templates.TemplateResponse("detected.html",
    {"request": request, "timestamp": timestamp})

@router.get("/render_add_page", response_class=HTMLResponse)
async def add(request: Request):
    print("==> Rendering add.html")  # Add this
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    return templates.TemplateResponse("add.html",
    {"request": request, "timestamp": timestamp})

@router.get("/render_update_page", response_class=HTMLResponse)
async def update(request: Request):
    print("==> Rendering update.html")  # Add this
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    return templates.TemplateResponse("update.html",
    {"request": request, "timestamp": timestamp})

@router.get("/render_summary_page", response_class=HTMLResponse)
async def summary(request: Request):
    print("==> Rendering summary.html")  # Add this
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    return templates.TemplateResponse("summary.html",
    {"request": request, "timestamp": timestamp})

@router.get("/get_daily_entries")
async def get_daily_entries():
    date_today = datetime.now().strftime('%Y-%m-%d')
    cursor.execute("SELECT * FROM loggedEntriesCount WHERE date = ?", (date_today,))
    row_data = cursor. fetchone()

    if row_data:
        result = {
            "date": row_data[0],
            "breakfastNum": row_data[1],
            "lunchNum": row_data[2],
            "dinnerNum": row_data[3],
            "snackNum": row_data[4]
        }
    else:
        result = {
            "date": date_today,
            "breakfastNum": 0,
            "lunchNum": 0,
            "dinnerNum": 0,
            "snackNum": 0
        }
    return JSONResponse(content=result)

@router.post("/start_entry")
async def start_entry(meal_category: str = Form(...)):
    print("==> In start entry!!!!")
    try:
        print("==> Creating new entry")
        entryCount = create_new_meal_entry(meal_category)

        return JSONResponse(entryCount)
    except Exception as e:
        print(f"{meal_category} not correct format!")
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/generate_summary_chart")
async def generate_chart():
    print("==> In generate chart")
    return JSONResponse({
        "labels": ["Chicken", "Noodles", "Cupcakes", "Peas", "Pies", "Yogurt"],
        "values": [5, 3, 7, 2, 4, 1]
    })

@router.post('/classify')
async def classify(image: UploadFile = File(...), dt: str = Form(...)):
    if not image:
        raise HTTPException(status_code=400, detail="No image uploaded")
    
    try:
        print("==> In classify in routes.py")
        contents = await image.read()
        image.file.seek(0)  # Reset file pointer after reading
        filename = image.filename
        
        print(f"==> Got file {image.filename}")
        processed_img = preprocess_image(image.file)

        # if image.filename == '':
        #     print(f"==> No selected file")
        #     return jsonify({"error": "No file selected"}, 400)

        filename = f"upload_{dt}.jpg"
        savePath = os.path.join(UPLOAD_FOLDER_PATH, filename)
        processed_img.save(savePath, format="JPEG")
        print("==> File saved successfully")

        output = run_inference(processed_img)
        cursor.execute("""
            UPDATE dailyLoggedEntries
            SET predictedItems = ?
            WHERE datetime = ?
        """), (json.dumps(output), dt)
        connect.commit()

        return JSONResponse(content={'message': "Image saved", "filename": filename, "output": output})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

        # return jsonify({'message': 'Image Saved!', 'filename': filename}, 200)

