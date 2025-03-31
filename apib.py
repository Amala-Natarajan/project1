import os
import requests
import sqlite3
from bs4 import BeautifulSoup
from PIL import Image
import speech_recognition as sr
import markdown
import pandas as pd
from fastapi import FastAPI, HTTPException, Query

# Base directory for data access
BASE_PATH ="D:\\IIT Diploma\\Tools in Data Science\\Project 1"


# Initialize FastAPI app
app = FastAPI()

# Ensure security compliance:
# B1: Only access files within /data
# B2: Prevent any data deletion


import sqlite3

def run_sql_query(database_file, query, output_file):
    db_path = os.path.join(BASE_PATH, database_file)
    output_path = os.path.join(BASE_PATH, output_file)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    result = cursor.execute(query).fetchone()  # Fetch single result
    conn.close()
    with open(output_path, "w") as f:
        f.write(str(result[0]))  # Write the fetched value

# B4: Clone a Git Repo and Make a Commit
def clone_and_commit(repo_url, local_dir, commit_message):
    repo_path = os.path.join(BASE_PATH, local_dir)
    from git import Repo  # Imported here to avoid unnecessary dependency if not used
    repo = Repo.clone_from(repo_url, repo_path)
    example_file = os.path.join(repo_path, "example.txt")
    with open(example_file, "w") as f:
        f.write("Automated commit message.")
    repo.index.add([example_file])
    repo.index.commit(commit_message)


# B5: Run a SQL Query on a SQLite/DuckDB Database
def run_sql_query(database_file, query, output_file):
    db_path = os.path.join(BASE_PATH, database_file)
    output_path = os.path.join(BASE_PATH, output_file)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    result = cursor.execute(query).fetchall()
    conn.close()
    with open(output_path, "w") as f:
        f.write(str(result))


# B6: Extract Data from a Website (Scrape)
def scrape_website(url, output_file):
    output_path = os.path.join(BASE_PATH, output_file)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    titles = [title.get_text() for title in soup.find_all("title")]
    with open(output_path, "w") as f:
        f.write("\n".join(titles))


# B7: Compress or Resize an Image
def compress_or_resize_image(input_image, output_image, size=(800, 800)):
    input_path = os.path.join(BASE_PATH, input_image)
    output_path = os.path.join(BASE_PATH, output_image)
    image = Image.open(input_path)
    image = image.resize(size)
    image.save(output_path, optimize=True, quality=85)


# B8: Transcribe Audio from an MP3 File
def transcribe_audio(input_audio, output_file):
    input_path = os.path.join(BASE_PATH, input_audio)
    output_path = os.path.join(BASE_PATH, output_file)
    recognizer = sr.Recognizer()
    with sr.AudioFile(input_path) as source:
        audio = recognizer.record(source)
    text = recognizer.recognize_google(audio)
    with open(output_path, "w") as f:
        f.write(text)


# B9: Convert Markdown to HTML
def convert_markdown_to_html(input_file, output_file):
    input_path = os.path.join(BASE_PATH, input_file)
    output_path = os.path.join(BASE_PATH, output_file)
    with open(input_path, "r") as f:
        markdown_content = f.read()
    html_content = markdown.markdown(markdown_content)
    with open(output_path, "w") as f:
        f.write(html_content)


# B10: Write an API Endpoint that Filters a CSV File and Returns JSON
@app.get("/filter-csv")
def filter_csv(column: str, value: str):
    file_path = os.path.join(BASE_PATH, "data.csv")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="CSV file not found")
    df = pd.read_csv(file_path)
    if column not in df.columns:
        raise HTTPException(status_code=400, detail="Column not found in CSV")
    filtered_df = df[df[column] == value]
    return filtered_df.to_dict(orient="records")