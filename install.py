import os
import requests
import zipfile
import sys
import platform

def download_chromedriver():
    # Determine the correct version to download based on the current system architecture
    system = platform.system()
    if system == 'Linux':
        chromedriver_version = '97.0.4692.71'
        download_url = f'https://chromedriver.storage.googleapis.com/{chromedriver_version}/chromedriver_linux64.zip'
    elif system == 'Darwin':
        chromedriver_version = '97.0.4692.71'
        download_url = f'https://chromedriver.storage.googleapis.com/{chromedriver_version}/chromedriver_mac64.zip'
    elif system == 'Windows':
        chromedriver_version = '97.0.4692.71'
        download_url = f'https://chromedriver.storage.googleapis.com/{chromedriver_version}/chromedriver_win32.zip'
    else:
        raise Exception(f'Unsupported system: {system}')

    # Download Chromedriver zip file
    print(f'Downloading Chromedriver version {chromedriver_version} for {system}...')
    response = requests.get(download_url)
    if response.status_code != 200:
        raise Exception(f'Failed to download Chromedriver: {response.status_code}')

    # Save zip file
    zip_file_path = 'chromedriver.zip'
    with open(zip_file_path, 'wb') as f:
        f.write(response.content)
    print('Chromedriver downloaded successfully.')

    # Extract Chromedriver executable
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall('.')

    # Make Chromedriver executable (for Linux/macOS)
    if system in ['Linux', 'Darwin']:
        os.chmod('chromedriver', 0o755)
        print('Chromedriver made executable.')

    # Clean up zip file
    os.remove(zip_file_path)
    print('Cleaned up temporary files.')

if __name__ == '__main__':
    try:
        download_chromedriver()
    except Exception as e:
        print(f'Error: {e}')
        sys.exit(1)
