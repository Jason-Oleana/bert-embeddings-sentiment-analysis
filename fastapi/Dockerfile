# Base image
FROM python:3.8-slim

# Set WORKDIR
WORKDIR /app

# Copy requirements
COPY ./fastapi-requirements.txt .

# Pip install requirements
RUN pip install -r fastapi-requirements.txt --no-cache-dir

# Create a models directory
RUN mkdir -p models

# Copy api.py
COPY ./api.py .

# CMD to run when container starts up
CMD ["uvicorn", "api:app","--host", "0.0.0.0", "--port", "8000", "--reload"]