import os
import requests

# Define API endpoints from Phase A
api_endpoints = {
    "install_uv": "install uv and run datagen",
    "format_markdown": "format markdown",
    "count_wednesdays": "count wednesdays",
    "sort_contacts": "sort contacts",
    "calculate_gold_ticket_sales": "calculate gold ticket sales"
}

# Define the secure data directory
DATA_DIR = "D:/IIT Diploma/Tools in Data Science/Project 1/data"
os.makedirs(DATA_DIR, exist_ok=True)  # Ensure directory exists

def fetch_and_save(api_name, task):
    """Send POST request to the API and save response."""
    try:
        response = requests.post("http://127.0.0.1:8000/run", json={"task": task})
        response.raise_for_status()  # Raise error if request fails

        file_path = os.path.join(DATA_DIR, f"{api_name}.json")

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(response.text)

        print(f"Saved data from {api_name} to {file_path}")

    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch {api_name}: {e}")

# Fetch data from all APIs using POST
for name, task in api_endpoints.items():
    fetch_and_save(name, task)
