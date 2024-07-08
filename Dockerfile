# Stage 1: Install dependencies
FROM python:3.9-slim AS build-stage
RUN apt update && apt install -y wget gnupg unzip

# Download and add Google signing key
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -

# Add Google Chrome repository
RUN echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list

# Update package lists again
RUN apt update

# Install Chrome and ChromeDriver
RUN apt install -y google-chrome-stable chromium-chromedriver

# Copy requirements.txt to build stage (optional)
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Final image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy application code and requirements (if not copied in build stage)
COPY requirements.txt .
COPY . .

# Run the Flask application with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:1010", "app:app"]
