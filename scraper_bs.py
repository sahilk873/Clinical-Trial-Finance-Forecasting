import requests
from bs4 import BeautifulSoup

def scrape_text_from_url_bs(url):
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract all text
        text = soup.get_text()
        
        # Return the extracted text
        return text.strip()
    else:
        return f"Failed to retrieve the URL."

