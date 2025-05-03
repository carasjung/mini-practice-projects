# News Summarizer
* A practice project for creating summmaries of news articles. This project uses BeautifulSoup to parse the news article and the summarization model from Hugging Face Transformers to generate summary.
* Since there is a token limit (1024 tokens), the program uses chunking to handle any large articles. 
* This program prompts user to provide the link to the article, checks if the article url is reachable (if the user no longer wants a summary, they can just input "quit" to exit the program), and offers a summary. 

## Installations
* Transformers: pip install transformers torch requests
* BeautifulSoup: pip install beautifulsoup4
* Rest of modules needed: re, requests, math

## Four functions
* Function for extracting text from news article 
    - Parse article using BeautifulSoup and extract the text
* Function for URL format
    - Use regex to check if the URL is a valid format
* Function for checking if the URL is actually reachable
    - Send HTTP GET request to check if the URL provided by the user is actually reachable
    - If it is, return status code 200 and if it isn't, return False
* Function for chunking text
    - Split the article into senteces by "." and collect sentence until it reaches the maximum number of tokens threshold (which is 1000)
    - Append the chunk into the 'chunks' list when it' full
    - Return the list

## Prompt user for URL
* Ask the user to input the URL. If it's not correctly formatted or unreachable keep asking. 
* Give the option to exit the program by typing in "quit"

## Extract text from URL and start chunking
* Use the function for extracting the text from the article. If the article is empty or is less than 100 words, exit.

## Summarize each chunk and combine
* Initialize a variable called chunk that stores a max of 1000 tokens
* Load the summarizer pipeline from Hugging Face
* Iterate through each chunk and append each result to the list full_summary
* Join and print the full summary comprised of individual chunk summary
