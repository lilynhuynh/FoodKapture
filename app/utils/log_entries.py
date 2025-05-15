"""
File: log_entries.py
Description: Creates foodKapture.db if it does not exist creates a new entry
into the table for all scanned entries.
"""

# Imports
import sqlite3
from datetime import datetime

# Connect to database (create if does not exist)
connect = sqlite3.connect("foodKapture.db", check_same_thread=True)
cursor = connect.cursor()

# Create TABLE for all logged meals
cursor.execute("""
    CREATE TABLE IF NOT EXISTS dailyLoggedEntries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        datetime TEXT NOT NULL,
        mealCategory TEXT NOT NULL,
        confirmedItems TEXT,
        caloriesList TEXT,
        fatsList TEXT,
        carbsList TEXT,
        proteinsList TEXT,
        amountsList TEXT
    )
""")
connect.commit()

# Create TABLE for daily logged meals count
cursor.execute("""
    CREATE TABLE IF NOT EXISTS loggedEntriesCount (
        date TEXT PRIMARY KEY,
        breakfastNum INTEGER DEFAULT 0,
        lunchNum INTEGER DEFAULT 0,
        dinnerNum INTEGER DEFAULT 0,
        snackNum INTEGER DEFAULT 0
    )
""")
connect.commit()


def create_new_meal_entry(category):
    """
    Given a meal category, it inserts a new logged entry that can be later updated based on the datetime.
    """
    print("==> Creating new entry in log_entries.py")

    current_meal_count = increment_meal_count(category)
    print("==> Received meal count", current_meal_count)

    datetime_str = datetime.now().strftime('%Y%m%d_%H%M%S')
    cursor.execute("""
        INSERT INTO dailyLoggedEntries (datetime, mealCategory)
        VALUES (?, ?)
    """, (datetime_str, category))
    connect.commit()

    print(f"==> Inserted NEW MEAL ENTRY: {datetime_str} | {category}")
    return datetime_str


def increment_meal_count(category):
    """
    When a new entry is created, it increments the given meal category.
    """
    print(f"==> In increment_meal_count for {category}!")

    date_today = datetime.now().strftime('%Y-%m-%d')
    print("==> Today's date:", date_today)

    cursor.execute("SELECT * FROM loggedEntriesCount WHERE date = ?", (date_today,))
    existing = cursor.fetchone()
    print("==> Today's date exist?", existing)

    # No row for today's datetime yet, create one
    if not existing:
        print(f"==> Row for {date_today} does NOT exist")
        cursor.execute(f"""
            INSERT INTO loggedEntriesCount (date, {category}Num)
            VALUES (?, 1)
        """, (date_today,))
    else:
        print(f"==> Row for {date_today} DOES exist")
        cursor.execute(f"""
            UPDATE loggedEntriesCount
            SET {category}Num = {category}Num + 1
            WHERE date = ?
        """, (date_today,))
    connect.commit()

    # Select updated row
    cursor.execute("SELECT * FROM loggedEntriesCount WHERE date = ?", (date_today,))
    updated_row = cursor.fetchone()
    print("==> New row!", updated_row)
    result = {
        "date": updated_row[0],
        "breakfastNum": updated_row[1],
        "lunchNum": updated_row[2],
        "dinnerNum": updated_row[3],
        "snackNum": updated_row[4]
    }
    print(f"==> Returned result! {result}")

    return result