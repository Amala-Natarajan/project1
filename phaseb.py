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

