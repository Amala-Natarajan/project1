from fastapi import FastAPI, HTTPException, Query
import os
import json
import sqlite3
import subprocess
from datetime import datetime
from pathlib import Path

# Set up FastAPI
app = FastAPI()

# Set directory path (Update this to your actual directory)
BASE_DIR = r"D:\IIT Diploma\Tools in Data Science\Project 1"

# Improved function for installing 'uv' and running 'datagen.py'
def install_uv_and_run_datagen():
    try:
        subprocess.run(["pip", "install", "uv"], check=True)
        subprocess.run(["python", f"{BASE_DIR}\\datagen.py", "24ds3000028ds.study.iitm.ac.in@"], check=True)
        return "uv installed and datagen.py executed."
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Error installing uv: {str(e)}")

format_path = Path(BASE_DIR) / "format.md"  # Better path handling

def format_markdown():
    try:
        subprocess.run(["npx", "prettier@3.4.2", "--write", str(format_path)], check=True, shell=True)
        return "Markdown formatted using Prettier."
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Error formatting markdown: {str(e)}")

# Improved function for counting Wednesdays
def count_wednesdays():
    try:
        input_path = os.path.join(BASE_DIR, "dates.txt")
        output_path = os.path.join(BASE_DIR, "dates-wednesdays.txt")

        if not os.path.exists(input_path):
            raise HTTPException(status_code=404, detail=f"File not found: {input_path}")

        # Supported date formats (with and without timestamps)
        date_formats = [
    "%Y-%m-%d", "%d-%m-%Y", "%m/%d/%Y", "%Y/%m/%d", "%d-%b-%Y",
    "%Y-%m-%d %H:%M:%S", "%d-%m-%Y %H:%M:%S", "%Y/%m/%d %H:%M:%S",
    "%b %d, %Y"  
]


        with open(input_path, "r") as f:
            dates = [line.strip() for line in f.readlines()]

        def parse_date(date_str):
            for fmt in date_formats:
                try:
                    return datetime.strptime(date_str, fmt).date()  # Extract only the date
                except ValueError:
                    continue
            raise ValueError(f"Unknown date format: {date_str}")

        count = sum(1 for date in dates if parse_date(date).weekday() == 2)

        with open(output_path, "w") as f:
            f.write(str(count))

        return f"Wednesdays counted: {count}"
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid date format: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error counting Wednesdays: {str(e)}")

# Improved function for sorting contacts
def sort_contacts():
    try:
        input_path = os.path.join(BASE_DIR, "contacts.json")
        output_path = os.path.join(BASE_DIR, "contacts-sorted.json")

        if not os.path.exists(input_path):
            raise HTTPException(status_code=404, detail=f"File not found: {input_path}")

        with open(input_path, "r") as f:
            try:
                contacts = json.load(f)
            except json.JSONDecodeError:
                raise HTTPException(status_code=400, detail="Invalid JSON format in contacts.json")

        sorted_contacts = sorted(contacts, key=lambda x: (x["last_name"], x["first_name"]))

        with open(output_path, "w") as f:
            json.dump(sorted_contacts, f, indent=2)

        return "Contacts sorted successfully."
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sorting contacts: {str(e)}")

# Improved function for calculating Gold ticket sales
def calculate_gold_ticket_sales():
    try:
        db_path = os.path.join(BASE_DIR, "ticket-sales.db")
        output_path = os.path.join(BASE_DIR, "ticket-sales-gold.txt")

        if not os.path.exists(db_path):
            raise HTTPException(status_code=404, detail=f"Database not found: {db_path}")

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Ensure the table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tickets';")
        if not cursor.fetchone():
            raise HTTPException(status_code=400, detail="Table 'tickets' does not exist in database")

        # Query to calculate total sales for Gold tickets
        cursor.execute("SELECT SUM(units * price) FROM tickets WHERE type = 'Gold'")
        total_sales = cursor.fetchone()[0] or 0
        conn.close()

        with open(output_path, "w") as f:
            f.write(str(total_sales))

        return f"Total Gold ticket sales: {total_sales}"
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating Gold ticket sales: {str(e)}")

#  Task Mapping
TASK_MAPPING = {
    "install uv and run datagen": install_uv_and_run_datagen,
    "format markdown": format_markdown,
    "count wednesdays": count_wednesdays,
    "sort contacts": sort_contacts,
    "calculate gold ticket sales": calculate_gold_ticket_sales,
}

# FastAPI Route for Running Tasks
@app.post("/run")
def run_task(task: str = Query(..., description="Task description")):
    task_lower = task.lower()
    for key, func in TASK_MAPPING.items():
        if key in task_lower:
            return {"status": "success", "message": func()}
    
    raise HTTPException(status_code=400, detail="Task not recognized.")

# FastAPI Route for Reading Files
@app.get("/read")
def read_file(path: str = Query(..., description="Relative file path from the base directory")):
    full_path = os.path.join(BASE_DIR, path)

    if not os.path.exists(full_path):
        raise HTTPException(status_code=404, detail=f"File not found: {full_path}")

    with open(full_path, "r", encoding="utf-8") as file:
        content = file.read()
    
    return {"status": "success", "content": content}



from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os
import json
import sqlite3
from PIL import Image
import markdown
import speech_recognition as sr
from bs4 import BeautifulSoup
import git
from typing import List, Dict

app = FastAPI()

# Security check to ensure all file paths are within /data
def is_within_data_directory(file_path: str) -> bool:
    return file_path.startswith('/data')

# Task handler functions (for example tasks)
def fetch_and_save(api_url: str, save_path: str):
    if not is_within_data_directory(save_path):
        raise HTTPException(status_code=400, detail="Cannot save data outside of /data directory.")
    
    response = requests.get(api_url)
    response.raise_for_status()  # Ensure successful request
    with open(save_path, 'w') as file:
        file.write(response.text)

def clone_and_commit(repo_url: str, commit_message: str, directory="/data"):
    if not is_within_data_directory(directory):
        raise HTTPException(status_code=400, detail="Cannot access repository outside of /data directory.")
    
    repo = git.Repo.clone_from(repo_url, directory)
    repo.git.add(A=True)
    repo.index.commit(commit_message)
    repo.remotes.origin.push()

def run_sqlite_query(database_path: str, query: str):
    if not is_within_data_directory(database_path):
        raise HTTPException(status_code=400, detail="Cannot access database outside of /data directory.")
    
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return result

def scrape_website(url: str):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup.prettify()

def resize_image(input_path, output_path, size=(800, 600)):
    with Image.open(input_path) as img:
        img = img.resize(size)
        img.save(output_path)

def transcribe_audio(mp3_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(mp3_file) as source:
        audio = recognizer.record(source)
    return recognizer.recognize_google(audio)

def convert_markdown_to_html(md_file):
    with open(md_file, 'r') as file:
        md_text = file.read()
    return markdown.markdown(md_text)

def filter_csv(csv_path: str, column_name: str, value: str):
    result = []
    with open(csv_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row[column_name] == value:
                result.append(row)
    return result


# Endpoint to execute a task based on description
@app.post("/run")
async def run_task(task: str):
    try:
        # Parse the task and execute corresponding function
        if "fetch data" in task:
            api_url = extract_api_url(task)
            save_path = "/data/api_data.txt"
            fetch_and_save(api_url, save_path)
            return {"message": "Data fetched and saved successfully."}
        
        elif "clone git" in task:
            repo_url = extract_repo_url(task)
            commit_message = "Automated commit"
            clone_and_commit(repo_url, commit_message)
            return {"message": "Git repository cloned and commit made."}
        
        elif "run SQL" in task:
            database_path = "/data/ticket-sales.db"
            query = "SELECT * FROM tickets WHERE type='Gold'"
            result = run_sqlite_query(database_path, query)
            return {"message": "SQL query executed.", "result": result}
        
        elif "scrape website" in task:
            url = extract_website_url(task)
            content = scrape_website(url)
            return {"message": "Website scraped successfully.", "content": content}
        
        elif "resize image" in task:
            resize_image("/data/input.jpg", "/data/output.jpg")
            return {"message": "Image resized successfully."}
        
        elif "transcribe audio" in task:
            transcription = transcribe_audio("/data/audio.mp3")
            return {"message": "Audio transcribed successfully.", "transcription": transcription}
        
        elif "convert markdown" in task:
            html_content = convert_markdown_to_html("/data/file.md")
            return {"message": "Markdown converted to HTML.", "html_content": html_content}
        
        elif "filter csv" in task:
            filtered_data = filter_csv("/data/data.csv", "status", "active")
            return {"message": "CSV file filtered successfully.", "filtered_data": filtered_data}
        
        else:
            raise HTTPException(status_code=400, detail="Unknown task description.")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Helper functions to extract information from the task descriptions
def extract_api_url(task: str):
    # Logic to extract the API URL from task description
    return "https://api.example.com/data"

def extract_repo_url(task: str):
    # Logic to extract the repo URL from task description
    return "https://github.com/example/repo.git"

def extract_website_url(task: str):
    # Logic to extract the website URL from task description
    return "https://example.com"

