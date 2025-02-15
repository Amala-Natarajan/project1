import re

# Read the email content
with open('D:\IIT Diploma\Tools in Data Science\Project 1\email.txt', 'r', encoding='utf-8') as file:
    email_content = file.read()

# Extract sender email using regex (assuming "From: <email>" format)
match = re.search(r"From: .*?([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]+)", email_content)

if match:
    sender_email = match.group(1)
    # Write the extracted email to the output file
    with open('D:\IIT Diploma\Tools in Data Science\Project 1\email-sender.txt', 'w', encoding='utf-8') as output_file:
        output_file.write(sender_email)

