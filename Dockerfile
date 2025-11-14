# Use the official Python image as the base image
FROM python:3.11.6-bookworm

# Set environment variables to avoid Python buffer issues
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements for faster builds
# Install system dependencies
# Install Python dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt /app/
# RUN apt-get install watch
# RUN pip install --upgrade pip && pip install -r requirements.txt
RUN  pip install --upgrade pip && pip install -U setuptools wheel && pip install cython && pip install -r requirements.txt
ENV MODE="production"
# Copy the application code into the working directory
COPY models/ /app/models/
COPY utils/install.sh /app/utils/
# COPY person_ner_server.py /app/
# install spacy model
RUN sh /app/utils/install.sh
# Expose the port that the FastAPI app will run on
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl --fail http://localhost:8000 || exit 1
# Run the FastAPI application
COPY loop.py /app/loop.py
#CMD ["uvicorn", "person_ner_server:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["python", "loop.py"]
