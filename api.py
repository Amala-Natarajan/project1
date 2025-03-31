import os
import subprocess
import json
import sqlite3
from datetime import datetime
from fastapi import FastAPI, HTTPException, Query
import re

# Define base directory for all files
BASE_PATH = "D:\\IIT Diploma\\Tools in Data Science\\Project 1"

# Initialize FastAPI app
app = FastAPI()


# Task A1: Install `uv` and run the `datagen.py` script
def task_a1(user_email):
    subprocess.run(["pip", "install", "uv"], check=True)
    subprocess.run(["python", os.path.join(BASE_PATH, "datagen.py"), user_email], check=True)

# Task A2: Format content using Prettier
def task_a2(file_path):
    subprocess.run(["npx", "prettier@3.4.2", "--write", os.path.join(BASE_PATH, file_path)], check=True)

# Task A3: Count Wednesdays in a file
def task_a3(input_file, output_file):
    input_path = os.path.join(BASE_PATH, input_file)
    output_path = os.path.join(BASE_PATH, output_file)

    # List of date formats to handle
    date_formats = ['%Y-%m-%d', '%d-%b-%Y', '%d/%m/%Y', '%m/%d/%Y']

    wednesdays = 0

    with open(input_path, "r") as f:
        dates = f.readlines()

    for date in dates:
        date = date.strip()  # Remove leading/trailing whitespace
        for fmt in date_formats:
            try:
                # Try to parse the date with the current format
                parsed_date = datetime.strptime(date, fmt)
                # Check if it's a Wednesday
                if parsed_date.weekday() == 2:
                    wednesdays += 1
                break  # Exit the loop once the date is successfully parsed
            except ValueError:
                continue  # Try the next format if parsing fails

    # Write the count of Wednesdays to the output file
    with open(output_path, "w") as f:
        f.write(str(wednesdays))

# Task A4: Sort contacts by last_name and first_name
def task_a4(input_file, output_file):
    input_path = os.path.join(BASE_PATH, input_file)
    output_path = os.path.join(BASE_PATH, output_file)
    with open(input_path, "r") as f:
        contacts = json.load(f)
    sorted_contacts = sorted(contacts, key=lambda x: (x["last_name"], x["first_name"]))
    with open(output_path, "w") as f:
        json.dump(sorted_contacts, f, indent=4)

# Task A5: Write first lines of 10 most recent log files
def task_a5(log_dir, output_file):
    log_path = os.path.join(BASE_PATH, log_dir)
    output_path = os.path.join(BASE_PATH, output_file)
    logs = sorted(
        (os.path.join(log_path, f) for f in os.listdir(log_path) if f.endswith(".log")),
        key=os.path.getmtime,
        reverse=True
    )[:10]
    with open(output_path, "w") as f:
        for log in logs:
            with open(log, "r") as lf:
                f.write(lf.readline())

# Task A6: Extract H1 titles from Markdown files
def task_a6(doc_dir, output_file):
    doc_path = os.path.join(BASE_PATH, doc_dir)
    output_path = os.path.join(BASE_PATH, output_file)
    index = {}
    for root, _, files in os.walk(doc_path):
        for file in files:
            if file.endswith(".md"):
                with open(os.path.join(root, file), "r") as f:
                    for line in f:
                        if line.startswith("# "):
                            index[file] = line.strip("# ").strip()
                            break
    with open(output_path, "w") as f:
        json.dump(index, f, indent=4)

# Task A7: Extract sender's email address from an email
def task_a7(input_file, output_file):
    input_path = os.path.join(BASE_PATH, input_file)
    output_path = os.path.join(BASE_PATH, output_file)

    # Read the email content from the input file
    with open(input_path, "r") as f:
        email_content = f.read()

    # Use a regular expression to extract email addresses
    email_matches = re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', email_content)

    # If multiple emails are found, assume the "From:" address is the sender
    sender_email = email_matches[0] if email_matches else "No email found"

    # Write the extracted email address to the output file
    with open(output_path, "w") as f:
        f.write(sender_email)


# Task A8: Extract credit card number from an image
def task_a8(input_image, output_file):
    image_path = os.path.join(BASE_PATH, input_image)
    output_path = os.path.join(BASE_PATH, output_file)
    prompt = f"Extract the credit card number from the image file located at {image_path}."
    card_number = call_llm(prompt)  # Replace with actual OCR/LLM integration
    with open(output_path, "w") as f:
        f.write(card_number)

# Task A9: Find the most similar comments using embeddings
def task_a9(input_file, output_file):
    input_path = os.path.join(BASE_PATH, input_file)
    output_path = os.path.join(BASE_PATH, output_file)
    with open(input_path, "r") as f:
        comments = f.readlines()
    prompt = "Find the two most similar comments in the following list:\n" + "\n".join(comments)
    similar_pair = call_llm(prompt)
    with open(output_path, "w") as f:
        f.write(similar_pair)

# Task A10: Calculate total sales for "Gold" ticket type
def task_a10(database_file, output_file):
    db_path = os.path.join(BASE_PATH, database_file)
    output_path = os.path.join(BASE_PATH, output_file)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(units * price) FROM tickets WHERE type = 'Gold'")
    total_sales = cursor.fetchone()[0]
    conn.close()
    with open(output_path, "w") as f:
        f.write(str(total_sales))

# Endpoint to execute tasks
@app.post("/run")
async def run_task(task: str = Query(..., description="Task description in plain English")):
    try:
        # Map task descriptions to functions
        if "install uv" in task.lower() and "datagen.py" in task.lower():
            user_email = task.split()[-1]
            task_a1(user_email)
            return {"status": "success", "message": "Task A1 completed"}

        elif "format" in task.lower():
            task_a2("format.md")
            return {"status": "success", "message": "Task A2 completed"}

        elif "count wednesdays" in task.lower():
            task_a3("dates.txt", "dates-wednesdays.txt")
            return {"status": "success", "message": "Task A3 completed"}

        elif "sort contacts" in task.lower():
            task_a4("contacts.json", "contacts-sorted.json")
            return {"status": "success", "message": "Task A4 completed"}

        elif "recent logs" in task.lower():
            task_a5("logs", "logs-recent.txt")
            return {"status": "success", "message": "Task A5 completed"}

        elif "extract h1" in task.lower():
            task_a6("docs", "docs-index.json")
            return {"status": "success", "message": "Task A6 completed"}

        elif "sender's email" in task.lower():
            task_a7("email.txt", "email-sender.txt")
            return {"status": "success", "message": "Task A7 completed"}

        elif "credit card number" in task.lower():
            task_a8("credit-card.png", "credit-card.txt")
            return {"status": "success", "message": "Task A8 completed"}

        elif "similar comments" in task.lower():
            task_a9("comments.txt", "comments-similar.txt")
            return {"status": "success", "message": "Task A9 completed"}

        elif "gold ticket sales" in task.lower():
            task_a10("ticket-sales.db", "ticket-sales-gold.txt")
            return {"status": "success", "message": "Task A10 completed"}

        else:
            raise HTTPException(status_code=400, detail="Task not recognized or not implemented")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to read file content
@app.get("/read")
async def read_file(path: str = Query(..., description="Path to the file to read")):
    full_path = os.path.join(BASE_PATH, path)
    if not os.path.exists(full_path):
        raise HTTPException(status_code=404, detail="File not found")

    with open(full_path, "r") as f:
        content = f.read()
    return {"status": "success", "content": content}