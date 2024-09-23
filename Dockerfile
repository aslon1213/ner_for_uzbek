# Use the official Python image as the base image
FROM python:3.11

# Set environment variables to avoid Python buffer issues
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements for faster builds
# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install fastapi[standard] deeppavlov spacy

# Copy the application code into the working directory
COPY . /app

# Expose the port that the FastAPI app will run on
# Run the FastAPI application
CMD ["fastapi" "run" "person_ner_server.py"]