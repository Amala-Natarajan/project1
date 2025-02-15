import os
import glob

# Define paths
log_dir = "d:/IIT Diploma/Tools in Data Science/Project 1/logs/"
output_file = "d:/IIT Diploma/Tools in Data Science/Project 1/logs-recent.txt"

try:
    # Get all .log files sorted by modification time (newest first)
    log_files = sorted(glob.glob(os.path.join(log_dir, "*.log")), key=os.path.getmtime, reverse=True)

    # Select the 10 most recent files
    recent_logs = log_files[:10]

    # Read the first line of each log file
    first_lines = []
    for log in recent_logs:
        with open(log, "r", encoding="utf-8") as f:
            first_line = f.readline().strip()  # Read first line and remove any trailing whitespace
            first_lines.append(first_line)

    # Write the collected first lines to output file
    with open(output_file, "w", encoding="utf-8") as f:
        for line in first_lines:
            f.write(line + "\n")

    print(f"Extracted first lines from 10 most recent log files. Output saved to {output_file}")

except FileNotFoundError:
    print("Error: Log directory not found.")
except Exception as e:
    print(f"Unexpected error: {e}")

