# Use the official Python image as the base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Install system-level dependencies (including Git)
RUN apt-get update && apt-get install -y \
    libsndfile1 \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements.txt into the container at /app
COPY requirements.txt /app/

# Install the dependencies inside the container
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files into the container
COPY . /app/

# Expose the application port (8000 for FastAPI)
EXPOSE 8000

# Command to run the FastAPI app with Uvicorn, binding it to all network interfaces (0.0.0.0) and on port 8000
CMD ["uvicorn", "create:app", "--host", "0.0.0.0", "--port", "8000"]
