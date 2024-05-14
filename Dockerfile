# Use a Python base image
FROM python:3.12-slim

RUN apt update
RUN apt install -y python3-pip
RUN pip3 install --upgrade pip

RUN pip3 install wheel

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install necessary dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the Flask app code into the container
COPY app.py .

# Expose the Flask default port
EXPOSE 5000

# Command to run the Flask app
CMD ["python", "app.py"]
