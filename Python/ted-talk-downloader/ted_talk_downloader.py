import time
import requests
import sys
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Set up Chrome options
chrome_options = Options() # Create an instance of Chrome settings
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--no-sandbox") # Improves stability
chrome_options.add_argument("--disable-dev-shm-usage") # Prevents memory allocation issues in Docker/Linux

# Initialize WebDriver (Single Instance)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
# ChromeDriverManager().install() auto-downloads and installs the right version of ChromeDriver
# Service(...) manages the Chrome WebDriver service
# options=chrome_options applies the custom Chrome settings (headless mode, etc)
# driver = webdriver.Chrome(...) creates a Chrome browser instance

# Get TED Talk URL from user input
if len(sys.argv) > 1:
    url = sys.argv[1]
else:
    sys.exit("Error: Please enter the TED Talk URL")

print("Opening TED Talk page...")
driver.get(url) # Opens TED Talk webpage in Chrome
time.sleep(3)  # Allow time for JavaScript to load

# Get page source and parse with BeautifulSoup
soup = BeautifulSoup(driver.page_source, "html.parser")
# driver.page_source fetches the full HTML of the TED Talk page
# BeautifulSoup(..., "html.parser") parses the HTML so we can search for elements

# Find the script tag containing JSON data
script_tag = None
for script in soup.find_all("script"):
    if "props" in script.text:
        script_tag = script.text
        break

# If no script tag found, exit
if not script_tag:
    driver.quit()
    sys.exit("Error: Unable to find video data on the page")

# Extract the MP4 URL using regex
mp4_match = re.search(r'https://[^"]+\.mp4', script_tag)

# If no match is found, quit
if not mp4_match:
    driver.quit()
    sys.exit("Error: Could not extract MP4 URL")

mp4_url = mp4_match.group(0) #.group(0) extracts the actual MP4 URL from the regex match

print(f"Downloading video from: {mp4_url}")

# Define filename
file_name = mp4_url.split("/")[-1].split("?")[0]
# mp4_url.split("/")[-1] gets the last part of the URL (filename)
# split("?")[0] removes any extra URL parameters

# Download the video
r = requests.get(mp4_url, stream=True) # Starts downloading the MP4 file in chunks
with open(file_name, 'wb') as f: # Opens the file in binary write mode 
    for chunk in r.iter_content(chunk_size=1024 * 1024): # Downloads 1MB chunks at a time
        if chunk:
            f.write(chunk) # Writes each chunk to the file

print(f"Download completed: {file_name}")

# Quit WebDriver at the very end
driver.quit()
