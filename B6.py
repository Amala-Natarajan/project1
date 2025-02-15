import requests
from bs4 import BeautifulSoup
import os

# Ensure the directory for data is within /data
DATA_DIR = 'D:/IIT Diploma/Tools in Data Science/Project 1'
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# URL to scrape
url = 'https://example.com'

# Send request to the website
response = requests.get(url)

# Parse the page content
soup = BeautifulSoup(response.text, 'html.parser')

# Extract relevant data (example: headlines)
headlines = soup.find_all('h2')

# Save the extracted data within the allowed directory
output_file = os.path.join(DATA_DIR, 'scraped_data.txt')

with open(output_file, 'w') as file:
    for headline in headlines:
        file.write(headline.text.strip() + '\n')

print(f"Data saved to {output_file}")
