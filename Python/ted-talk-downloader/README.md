## Ted Talk Downloader
This is a project based on Ted Talk Downloader tutorial from freeCodeCamp with the following adjustments:
* Original project used Requests and BeautifulSoup bus since the tutorial was posted, the TED website has made changes and now generates video URLs dynamically via Javascript. The original code fetched the initial page HTML but since the url is no longer present in the raw HTML, it doesn't work
* This modified version uses Selenium to load the JavaScript content and extract the MP4 URL
* The original code is faster since it makes a direct HTTP request and uses low memory since it requires no browser overhead. But it doesn't work.

Below is an overview of the code's structure

# Import all modules and libraries
* For this project we will be using the following:
    * time - To allow time for Javascript to load
    * requests - For downloading the video
    * sys - To get the TED URL from user
    * bs4 - To use BeautifulSoup to parse the page source
    * selenium - To use webdriver for Chrome. We will use it to set up the Chrome options and service. We will also use ChromeDriverManager so the program automatically downloads and installs the right version of ChromeDriver instead of manually doing it

# Set up Chrome options
* Set up Chrome options. For this program, we will: 
    * Run in headless mode to run Chrome without GUI
    * Not use sandbox to improve stability
    * Prevent using shared memory. Using shared memory can cause issues in Docker containers and Linux environments since by default, Docker limits /dev/shm to 64MB and Chrome uses more than that. This can cause crashes, timeouts, etc.

# Initialize WebDriver with the Chrome options
* Initialize Selenium WebDriver with the custom options (headless, no-sandbox, /dev/shm disabled)
* Create Service for WebDriver, which will wrap ChromeDriver into a service that Selenium can use
* The ChromeDriverManager().install() will automatically download the correct version of the ChromeDriver for your Chrome

# Prompt the user for the TED Talk URL
* Ask user for the TED Talk URL. If they don't provide one, exit
* Open the TED Talk page in Chrome and use time.sleep() to allow time for Javascript to load

# Get page source and parse with BeautifulSoup
* Get the full HTML of the TED Talk page and use BeautifulSoup to parse the HTML

# Find the script tag containing the JSON data
* Initialize script_tag to None so in case no matches are found, it will remain None. This will be useful to help detect errors in the future
* The <script> tag  with "props" will have the JSON data that contains the MP4 video URL
* Once the match is found, it will store the content into the script_tag variable and stop the search

# Extract the MP4 URL using regex
* Use regex to search the content in the script_tag for the MP4 link

# Extract clean filename
* Split the URL by slashes and turn them into a list so you can extract the last part
* Remove the query parameters at the end (i.e. ?apikey=123)
* The result should be a clean filename like 'videoName.mp4'

# Download the video
* Send the HTTP GET request to download the video from the mp4_url
* Open a new file called file_name in 'wb' mode since videos are non-text (binary files)
* Download the video in chunks of 1MB at a time (for stable download)
