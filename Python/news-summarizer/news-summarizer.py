import re
import requests
import math
from transformers import pipeline
from bs4 import BeautifulSoup

# Extract text from article's URL
def extract_article_text(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser') # Parse HTML
    paragraphs = soup.find_all('p') # Find all <p> tags wrapping article text
    text = ' '.join(p.get_text() for p in paragraphs) # Extract the text and join them
    return text

# URL regex
def valid_url_format(url):
    regex = re.compile(
        r'^https?:\/\/'                         # Start with http:// or https://
        r'(([A-Za-z0-9-]+\.)+[A-Za-z]{2,6})'    # Domain
        r'(\/\S*)?$'                            # Optional path
    )
    return re.match(regex, url) is not None

# Check if the url works
def url_works(url):
    try:
        response = requests.get(url, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False

# Split long text into chunks
def chunk_text(text, max_tokens=1000):
    sentences = text.split('. ')
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len((current_chunk + sentence).split()) < max_tokens:
            current_chunk += sentence + ". "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + ". "
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks
 
# Ask user for a valid article link. Give them the option to quit if they wish
while True:
    url = input("Enter the article URL you want to summarize or type 'quit' if you want to exit: ").strip()
    if url.lower() == "quit":
        exit()
    if not valid_url_format(url):
        print("Not a valid URL format. Please try again or type 'quit' to exit the program: ")
        continue
    if not url_works(url):
        print("The URL you entered can't be reached. Please try another one or type 'quit' to exit the program: ")
        continue
    break

# Extract text from URL
text = extract_article_text(url)
if not text or len(text.strip()) < 100:
    print("The article is too short or empty. Exiting.")
    exit()

# Chunk the text
chunks = chunk_text(text, max_tokens=1000)

# Load summarizer pipeline
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Summarize each chunk and combine
print(f"\nSummarizing {len(chunks)} chunk(s)...\n")
full_summary = []
for i, chunk in enumerate(chunks, 1):
    summary = summarizer(chunk, max_length=130, min_length=30, do_sample=False)
    print(f"Chunk {i} summary complete")
    full_summary.append(summary[0]['summary_text'])

# Print the summary
print("\nFull Article Summary: \n")
print(' '.join(full_summary))