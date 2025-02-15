import os

BASE_DIR = r"D:\IIT Diploma\Tools in Data Science\Project 1"

def is_safe_path(file_path):
    """ Ensure the file path is inside the base directory """
    abs_path = os.path.abspath(file_path)
    return abs_path.startswith(BASE_DIR)

def read_file(file_path):
    """ Read a file only if it is inside the base directory """
    if not is_safe_path(file_path):
        raise PermissionError("Access denied: Attempt to read outside the project directory")
    
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

def write_file(file_path, content):
    """ Write to a file only if it is inside the base directory """
    if not is_safe_path(file_path):
        raise PermissionError("Access denied: Attempt to write outside the project directory")
    
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)

# Example usage
try:
    safe_path = os.path.join(BASE_DIR, "sample.txt")
    write_file(safe_path, "Hello, DataWorks!")
    print(read_file(safe_path))

    # This should fail
    read_file(r"C:\Windows\System32\config.sys")  
except PermissionError as e:
    print(e)

