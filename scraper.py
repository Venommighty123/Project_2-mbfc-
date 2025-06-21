import csv
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
# from transformers import pipeline
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from googlesearch import search  # pip install googlesearch-python
from webdriver_manager.chrome import ChromeDriverManager

def clean_body_content(html):
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style"]):
        tag.decompose()
    paragraphs = soup.find_all("p")
    return "\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))


def scrape_website(url):
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get(url)
        time.sleep(7)
        return driver.page_source
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return ""
    finally:
        driver.quit()