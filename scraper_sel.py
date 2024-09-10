from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def scrape_text_from_url_sel(url):
    # Set up the WebDriver (you can replace ChromeDriverManager with the path to your local driver if needed)
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode (without opening a browser window)
    driver = webdriver.Chrome(service=service, options=options)
    
    # Open the URL
    driver.get(url)
    
    # Extract the text content of the entire page
    text = driver.find_element(By.TAG_NAME, 'body').text
    
    # Close the browser
    driver.quit()
    
    return text

# Example usage
u'''rl = "https://ecog-acrin.org/clinical-trials/ea8191-indicate-prostate-cancer/"
text = scrape_text_from_url(url)
print(text)'''
