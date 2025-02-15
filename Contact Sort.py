import json

# Define file paths
input_file = "d:/IIT Diploma/Tools in Data Science/Project 1/contacts.json"
output_file = "d:/IIT Diploma/Tools in Data Science/Project 1/contacts-sorted.json"

try:
    # Read the JSON file
    with open(input_file, "r", encoding="utf-8") as f:
        contacts = json.load(f)

    # Ensure the contacts list is not empty and contains dictionaries
    if not isinstance(contacts, list):
        raise ValueError("JSON structure is not a list.")

    # Sort contacts by last_name, then first_name
    sorted_contacts = sorted(contacts, key=lambda x: (x.get("last_name", "").lower(), x.get("first_name", "").lower()))

    # Write the sorted contacts to a new JSON file
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(sorted_contacts, f, indent=4)

    print(f"Contacts sorted successfully. Output saved to {output_file}")

except FileNotFoundError:
    print(f"Error: File {input_file} not found.")
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {input_file}.")
except Exception as e:
    print(f"Unexpected error: {e}")

