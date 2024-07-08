# Stage 1: Install dependencies and build stage
FROM python:3.9-slim AS build-stage

# Install system dependencies
RUN apt-get update && \
    apt-get install -y wget gnupg unzip

# Install ChromeDriver
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y chromium-chromedriver

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

# Copy application code and requirements from build stage
# Identify specific ChromeDriver dependencies
RUN ldd /usr/bin/chromedriver | awk '/chromium/{print $3}' | xargs -I {} cp --from=build-stage /usr/lib/chromium/{} /usr/lib/chromium/{}

# Copy application code
COPY --from=build-stage /app .

# Run the Flask application with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:1010", "app:app"]
