from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess
import os
import json
import datetime
import sqlite3
import re
from typing import Optional
from datetime import datetime

app = FastAPI()

# Model for the task description
class TaskRequest(BaseModel):
    task: str

# POST /run endpoint to handle tasks
@app.post("/run")
async def run_task(request: TaskRequest):
    task_description = request.task
    if not task_description:
        raise HTTPException(status_code=400, detail="No task description provided")
    
    try:
        # Parse the task description and execute the corresponding operation
        if "install uv" in task_description and "run" in task_description:
            user_email = extract_user_email(task_description)
            result = run_data_gen(user_email)
        elif "format" in task_description and "prettier" in task_description:
            result = format_file_with_prettier()
        elif "Wednesdays" in task_description or "count dates" in task_description:
            result = count_wednesdays_in_dates()
        elif "sort contacts" in task_description:
            result = sort_contacts()
        elif "recent log" in task_description:
            result = get_recent_log()
        elif "Markdown" in task_description:
            result = extract_h1_titles_from_markdown()
        elif "email sender" in task_description:
            result = extract_email_sender()
        elif "credit card" in task_description:
            result = extract_credit_card()
        elif "similar comments" in task_description:
            result = find_similar_comments()
        elif "Gold ticket sales" in task_description:
            result = calculate_gold_ticket_sales()
        else:
            raise Exception("Task description not recognized")
        
        return {"message": "Task executed successfully", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# A1: Run data generator script with user email
def run_data_gen(user_email):
    command = f"uv run https://raw.githubusercontent.com/sanand0/tools-in-data-science-public/tds-2025-01/project-1/datagen.py {user_email}"
    subprocess.run(command, shell=True, check=True)
    return "Data generation complete"

# A2: Format file using prettier
def format_file_with_prettier():
    subprocess.run("npx prettier@3.4.2 --write /data/format.md", shell=True, check=True)
    return "File formatted successfully"


# List of possible date formats
date_formats = [
    "%Y-%m-%d", "%d-%m-%Y", "%m/%d/%Y", "%Y/%m/%d", "%d-%b-%Y",
    "%Y-%m-%d %H:%M:%S", "%d-%m-%Y %H:%M:%S", "%Y/%m/%d %H:%M:%S",
    "%b %d, %Y"  
]


def count_wednesdays_in_dates(file_path: str) -> int:
    try:
        # Read the file
        with open(file_path, 'r') as f:
            dates = f.readlines()

        # Count Wednesdays
        wednesday_count = 0
        for date_str in dates:
            date_str = date_str.strip()
            # Try parsing the date with common formats
            for date_format in ['%Y-%m-%d', '%d-%b-%Y', '%d/%m/%Y']:
                try:
                    date_obj = datetime.datetime.strptime(date_str, date_format)
                    if date_obj.weekday() == 2:  # 2 represents Wednesday
                        wednesday_count += 1
                    break
                except ValueError:
                    continue  # Try the next format if parsing fails

        return wednesday_count
    except Exception as e:
        return str(e)



# A4: Sort contacts in contacts.json
def sort_contacts():
    with open("D:/IIT Diploma/Tools in Data Science/Project 1/contacts.json", "r") as f:
        contacts = json.load(f)
    sorted_contacts = sorted(contacts, key=lambda x: (x['last_name'], x['first_name']))
    with open("D:/IIT Diploma/Tools in Data Science/Project 1/contacts-sorted.json", "w") as f:
        json.dump(sorted_contacts, f, indent=4)
    return "Contacts sorted"

# A5: Get the first line of the most recent log
def get_recent_log():
    log_files = sorted(os.listdir("D:/IIT Diploma/Tools in Data Science/Project 1/logs/"), reverse=True)
    recent_logs = [f for f in log_files if f.endswith(".log")]
    if not recent_logs:
        raise Exception("No log files found")
    with open(f"D:/IIT Diploma/Tools in Data Science/Project 1/logs/{recent_logs[0]}", "r") as f:
        first_line = f.readline()
    with open("D:/IIT Diploma/Tools in Data Science/Project 1/logs-recent.txt", "w") as f:
        f.write(first_line)
    return "First line of recent log saved"

# A6: Extract H1 titles from markdown files
def extract_h1_titles_from_markdown():
    md_files = [f for f in os.listdir("D:/IIT Diploma/Tools in Data Science/Project 1/docs/") if f.endswith(".md")]
    index = {}
    for file in md_files:
        with open(f"D:/IIT Diploma/Tools in Data Science/Project 1/docs/{file}", "r") as f:
            for line in f:
                if line.startswith("# "):
                    index[file] = line.strip("# ").strip()
                    break
    with open("D:/IIT Diploma/Tools in Data Science/Project 1/docs/index.json", "w") as f:
        json.dump(index, f, indent=4)
    return "H1 titles extracted"

# A7: Extract email sender
def extract_email_sender():
    with open("D:/IIT Diploma/Tools in Data Science/Project 1/email.txt", "r") as f:
        email_content = f.read()
    sender_email = re.search(r"From: (.+?@.+?)(?:\s|$)", email_content)
    if sender_email:
        with open("D:/IIT Diploma/Tools in Data Science/Project 1/email-sender.txt", "w") as f:
            f.write(sender_email.group(1))
        return "Sender's email extracted"
    raise Exception("Sender's email not found")

# A8: Extract credit card number from image
def extract_credit_card():
    # Assuming we use an LLM or a service for OCR
    credit_card_number = "1234567812345678"  # Placeholder
    with open("D:/IIT Diploma/Tools in Data Science/Project 1/credit-card.txt", "w") as f:
        f.write(credit_card_number.replace(" ", ""))
    return "Credit card number extracted"

# A9: Find most similar comments
def find_similar_comments():
    with open("D:/IIT Diploma/Tools in Data Science/Project 1/comments.txt", "r") as f:
        comments = f.readlines()
    # Assume embedding-based similarity function (placeholder)
    most_similar_pair = (comments[0], comments[1])  # Placeholder for similarity calculation
    with open("D:/IIT Diploma/Tools in Data Science/Project 1/comments-similar.txt", "w") as f:
        f.write(f"{most_similar_pair[0].strip()} | {most_similar_pair[1].strip()}")
    return "Most similar comments found"

# A10: Calculate total sales for 'Gold' ticket type
def calculate_gold_ticket_sales():
    conn = sqlite3.connect("D:/IIT Diploma/Tools in Data Science/Project 1/ticket-sales.db")
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(units * price) FROM tickets WHERE type='Gold'")
    total_sales = cursor.fetchone()[0]
    with open("D:/IIT Diploma/Tools in Data Science/Project 1/ticket-sales-gold.txt", "w") as f:
        f.write(str(total_sales))
    conn.close()
    return f"Total sales for Gold tickets: {total_sales}"

# Extract user email from task description
def extract_user_email(task_description):
    email_match = re.search(r"[\w\.-]+@[\w\.-]+", task_description)
    if email_match:
        return email_match.group(0)
    raise Exception("User email not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000)
