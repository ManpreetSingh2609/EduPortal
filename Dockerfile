# Stage 1: Install dependencies and build stage
FROM python:3.9-slim AS build-stage

# Install system dependencies
RUN apt-get update && \
    apt-get install -y wget gnupg unzip

# Install Python dependencies
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

# Install gunicorn
RUN pip install gunicorn

# Stage 2: Final image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy application code
COPY --from=build-stage /app .

# Run the Flask application with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:1010", "app:app"]
