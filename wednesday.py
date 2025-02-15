import datetime

# Define file paths
input_file = "d:/IIT Diploma/Tools in Data Science/Project 1/dates.txt"
output_file = "d:/IIT Diploma/Tools in Data Science/Project 1/dates-wednesdays.txt"

# Possible date formats to handle mixed formats
date_formats = [
    "%d-%b-%Y",     # Example: 14-Jan-2019
    "%Y-%m-%d",     # Example: 2019-01-14
    "%Y/%m/%d",     # Example: 2019/01/14
    "%Y/%m/%d %H:%M:%S",  # Example: 2009/05/09 05:10:01
    "%d/%m/%Y",     # Example: 14/01/2019
]

def parse_date(date_str):
    """Try multiple formats to parse the date."""
    for fmt in date_formats:
        try:
            return datetime.datetime.strptime(date_str.strip(), fmt)
        except ValueError:
            continue
    return None  # Return None if no format matches

try:
    # Read the file and count Wednesdays 
    with open(input_file, "r") as f:
        wednesday_count = sum(1 for line in f if (dt := parse_date(line)) and dt.weekday() == 2)

    # Write the result to the output file :
    with open(output_file, "w") as f:
        f.write(str(wednesday_count) + "\n")

    print(f"Count of Wednesdays: {wednesday_count} (written to {output_file})")

except FileNotFoundError:
    print(f"Error: File {input_file} not found.")
except Exception as e:
    print(f"Unexpected error: {e}")
