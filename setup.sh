#!/usr/bin/env bash

# Install Chrome browser
echo "Installing Google Chrome"
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | sudo tee -a /etc/apt/sources.list.d/google-chrome.list
sudo apt-get update
sudo apt-get install -y google-chrome-stable

# Install Chromedriver
echo "Installing Chromedriver"
wget -N https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip -P ~/
unzip ~/chromedriver_linux64.zip -d ~/
sudo mv -f ~/chromedriver /usr/local/bin/chromedriver
sudo chmod +x /usr/local/bin/chromedriver
rm ~/chromedriver_linux64.zip

echo "setup.sh script completed!"