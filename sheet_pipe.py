# Use the official Python image from the Docker Hub
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Install git
RUN apt-get update && apt-get install -y git

# Clone your GitHub repository
RUN git clone https://github.com/jinxlo/sheet_pipline.git

# Change directory to your repository
WORKDIR /app/sheet_pipline

# Install the dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r /app/sheet_pipline/requirements.txt

# Command to run your pipeline script
CMD ["python", "pipeline.py"]
