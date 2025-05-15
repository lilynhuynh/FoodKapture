"""
File: routes.py
Description: Configures all the POST and GET API routes.

Bugs: Not really a bug but this code is using a placeholder yolo model and
dummy nutritional values as there were some complications trying to connect
the model through a Hugging Face API
"""

# Imports
from fastapi import APIRouter, Request, UploadFile, File, HTTPException, Form
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
import os
from .utils.log_entries import create_new_meal_entry
from .model.predict import run_inference
import sqlite3
import json
from datetime import datetime
from PIL import Image
import httpx
import time

# Create API router instance
router = APIRouter()

# Set up directory paths
BASE_DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIRECTORY = os.path.join(BASE_DIRECTORY, 'templates')
templates = Jinja2Templates(directory=TEMPLATES_DIRECTORY)
UPLOAD_FOLDER_PATH = os.path.join(os.path.dirname(__file__), "..", "uploads")
os.makedirs(UPLOAD_FOLDER_PATH, exist_ok=True)

# Connect to database
connect = sqlite3.connect("foodKapture.db")
cursor = connect.cursor()


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """
    Renders the index.html home page and returns a timestamp
    """
    print("==> Rendering index.html")
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    return templates.TemplateResponse("index.html",
    {"request": request, "timestamp": timestamp})


@router.get("/render_scan_page", response_class=HTMLResponse)
async def scan(request: Request):
    """
    Renders the scan.html home page and returns a timestamp
    """
    print("==> Rendering scan.html")
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    return templates.TemplateResponse("scan.html",
    {"request": request, "timestamp": timestamp})


@router.get("/render_detected_page", response_class=HTMLResponse)
async def detect(request: Request):
    """
    Renders the detected.html home page and returns a timestamp
    """
    print("==> Rendering detected.html")
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    return templates.TemplateResponse("detected.html",
    {"request": request, "timestamp": timestamp})


@router.get("/render_add_page", response_class=HTMLResponse)
async def add(request: Request):
    """
    Renders the add.html home page and returns a timestamp
    """
    print("==> Rendering add.html")
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    return templates.TemplateResponse("add.html",
    {"request": request, "timestamp": timestamp})


@router.get("/render_summary_page", response_class=HTMLResponse)
async def summary(request: Request):
    """
    Renders the summary.html home page and returns a timestamp
    """
    print("==> Rendering summary.html")
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    return templates.TemplateResponse("summary.html",
    {"request": request, "timestamp": timestamp})


@router.post("/generate_summary_chart")
async def generate_chart(request: Request):
    """
    Gets the daily meals entries and returned the daily meal summary of all
    food items, total calories, fats, carbs, and proteins recorded for the day
    """
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
            labelInstances[item] = test_data[item]["amount"]
        else:
            labelInstances[item] = labelInstances[item] + test_data[item]["amount"]

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


@router.get("/get_daily_entries")
async def get_daily_entries():
    """
    Based on the current date, it will grab all logged entries for that date
    from the database and return the current number of each entry for each
    meal category
    """
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
    """
    When a new image entry is submitted it creates a new entry in the SQL
    table and calls classify to get a list of detected items and its
    nutritional values
    """
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


async def classify(image: UploadFile, dt: str):
    """
    Helper function that calls the predict.py in model to get the detected
    items from the model and get its nutritional values

    NOTE - Currently using placeholder yolov5 model and placeholder nutritional
    values
    """
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

        # NOTE - Attempted to connect to hugging face api
        # url = "https://lilynhuynh-foodkapture-fastapi.hf.space/predict/"
        # print("==> Sending request to Hugging Face Space...")
        # start = time.time()
        # files = {"file": (filename, contents, "image/jpeg")}
        # async with httpx.AsyncClient(timeout=60.0) as client:
        #     response = await client.post(url, files=files)
        # duration = time.time() - start
        # print(f"==> Response received in {duration:.2f} seconds")
        # if response.status_code != 200:
        #     raise Exception(f"HF API failed: {response.status_code} - {response.text}")

        food_items = list(testoutput.keys())
        calories = [testoutput[item]['calories'] for item in food_items]
        fats = [testoutput[item]['fats'] for item in food_items]
        carbs = [testoutput[item]['carbs'] for item in food_items]
        proteins = [testoutput[item]['proteins'] for item in food_items]
        amounts = [testoutput[item]['amount'] for item in food_items]
        
        cursor.execute("""
            UPDATE dailyLoggedEntries
            SET
                confirmedItems = ?,
                caloriesList = ?,
                fatsList = ?,
                carbsList = ?,
                proteinsList = ?,
                amountsList = ?
            WHERE datetime = ?
        """, (
            json.dumps(food_items),
            json.dumps(calories),
            json.dumps(fats),
            json.dumps(carbs),
            json.dumps(proteins),
            json.dumps(amounts),
            dt
        ))
        connect.commit()

        return {
            'message': "Image saved and sent to hugging face",
            'filename': filename,
            'output': testoutput
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def testInput(prediction: list):
    """
    Placeholder helper function that returns dummy nutritional values from the
    detected values from the predicted list. Currently can only handle
    hot dog, apple, and donut
    """
    print("==> In test", prediction)

    testJSON = {}

    for item in prediction:
        if item == "hot dog":
            testJSON[item] = {
                'calories': 215,
                'fats': 18.9,
                'carbs': 0.3,
                'proteins': 10.3,
                'amount': 2
            }
        if item == "apple":
            testJSON[item] = {
                'calories': 95,
                'fats': 0,
                'carbs': 25,
                'proteins': 1,
                'amount': 1
            }
        if item == "donut":
            testJSON[item] = {
                'calories': 272,
                'fats': 12,
                'carbs': 38.8,
                'proteins': 3.8,
                'amount': 5
            }

    test_data = testJSON
    print("==> Test Output:", testJSON)
    print(json.dumps(testJSON))
    return testJSON

