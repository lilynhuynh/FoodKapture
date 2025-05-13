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
from PIL import Image

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

@router.post("/generate_summary_chart")
async def generate_chart(request: Request):
    print("==> In generate chart")
    data = await request.json()
    test_data = data.get('output')

    print("==> Saved data", test_data)

    # TODO - add SQL implementation
    labelNames = []
    labelInstances = {}
    totalCals = 0
    totalFats = 0
    totalCarbs = 0
    totalProteins = 0

    for item, values in test_data.items(): # for each key
        print("==> Current item:", item, values)
        if item not in labelInstances:
            labelNames.append(item)
            labelInstances[item] = 1
        else:
            labelInstances[item] = labelInstances[item] + 1
        totalCals += values["calories"]
        totalFats += values["fats"]
        totalCarbs += values["carbs"]
        totalProteins += values["proteins"]

    result = {
        "labels": labelNames,
        "values": list(labelInstances.values()),
        "cals": totalCals,
        "fats": totalFats,
        "carbs": totalCarbs,
        "proteins": totalProteins
    }
    print("==> Current returning summary table", result)
    return result


    return JSONResponse(content={
        "labels": test_data.keys(),
        "values": [5, 3, 7, 2, 4, 1],
        "cals": totalCals,
        "fats": totalFats,
        "carbs": totalCarbs,
        "proteins": totalProteins
    })

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
async def start_entry(meal_category: str = Form(...), image: UploadFile = File(...)):
    print("==> In start entry!!!!")
    try:
        print("==> Creating new entry")
        datetime_entry = create_new_meal_entry(meal_category)
        print("==> Received datetime from create new entry:", datetime_entry)

        detected_items = await classify(image, datetime_entry)

        return JSONResponse(content=detected_items)
    except Exception as e:
        print(f"{meal_category} not correct format!")
        raise HTTPException(status_code=500, detail=str(e))

# @router.post('/classify')
async def classify(image: UploadFile, dt: str):
    if not image:
        raise HTTPException(status_code=400, detail="No image uploaded")
    
    try:
        print("==> In classify in routes.py")
        contents = await image.read()
        image.file.seek(0)  # Reset file pointer after reading
        filename = image.filename
        
        print(f"==> Got file {image.filename}")
        processed_img = (Image.open(image.file)).convert("RGB")

        filename = f"upload_{dt}.jpg"
        print(f"==>Expected upload name: {filename}")
        savePath = os.path.join(UPLOAD_FOLDER_PATH, filename)
        processed_img.save(savePath, format="JPEG")
        print("==> File saved successfully")

        output = run_inference(processed_img)
        print("==> Received prediction:", output)
        testoutput = await testInput(output)
        print("==> Received testoutput", testoutput)
        # cursor.execute("""
        #     UPDATE dailyLoggedEntries
        #     SET predictedItems = ?
        #     WHERE datetime = ?
        # """), (json.dumps(output), dt)
        # connect.commit()

        return {
            'message': "Image saved",
            'filename': filename,
            'output': testoutput
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def testInput(prediction: list):
    print("==> In test", prediction)

    testJSON = {}

    for item in prediction:
        if item == "hot dog":
            testJSON[item] = {
                'calories': 215,
                'fats': 18.9,
                'carbs': 0.3,
                'proteins': 10.3
            }
        if item == "apple":
            testJSON[item] = {
                'calories': 95,
                'fats': 0,
                'carbs': 25,
                'proteins': 1
            }
        if item == "donut":
            testJSON[item] = {
                'calories': 272,
                'fats': 12,
                'carbs': 38.8,
                'proteins': 3.8
            }

    test_data = testJSON
    print("==> Test Output:", testJSON)
    print(json.dumps(testJSON))
    return testJSON

