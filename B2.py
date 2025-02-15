import os

# Override os.remove to prevent deletion
def prevent_deletion(*args, **kwargs):
    raise PermissionError("File deletion is not allowed.")

os.remove = prevent_deletion
os.unlink = prevent_deletion  # Also blocks os.unlink()

# Test
try:
    os.remove("D:\\IIT Diploma\\Tools in Data Science\\Project 1\\hi.txt")
except PermissionError as e:
    print(e)  # This will print "File deletion is not allowed."
