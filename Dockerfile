# Stage 1: Install dependencies and build stage
FROM python:3.9-slim AS build-stage

# Install system dependencies
RUN apt-get update && \
    apt-get install -y wget gnupg unzip

# Install Chrome and ChromeDriver
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get update
RUN apt-get install -y google-chrome-stable chromium-chromedriver

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

# Copy application code and requirements
COPY --from=build-stage /usr/bin/chromedriver /usr/bin/chromedriver
COPY --from=build-stage /usr/lib/chromium/chromedriver /usr/lib/chromium/chromedriver
COPY --from=build-stage /app .

# Run the Flask application with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:1010", "app:app"]
