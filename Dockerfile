# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install the necessary packages
RUN pip install --no-cache-dir -r requirements.txt

# Install Chrome browser
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' \
    && apt-get update \
    && apt-get install -y google-chrome-stable

# Add the ChromeDriver to the path
ENV PATH="/app/drivers:${PATH}"

# Make port 1010 available to the world outside this container
EXPOSE 1010

# Run Gunicorn to serve the Flask app
CMD ["gunicorn", "--bind", "0.0.0.0:1010", "app:app"]
