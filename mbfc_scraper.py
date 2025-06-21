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

def scrape_website_mbfc(url):
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()  # Raises HTTPError for bad responses (4xx or 5xx)
        return resp.text
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return ""

def clean_body_content_mbfc(html):
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style"]):
        tag.decompose()
    return "\n".join(line.strip() for line in soup.get_text(separator="\n").splitlines() if line.strip())

# Factual Reporting score from mbfc website
def fetch_mbfc_factual_score(domain):
    for substr in [".", "/", "-", "www", "org", "en", "com"]:
        domain = domain.replace(substr, "")
    domain = domain.lower()
    search_url = f"{domain} media bias fact check"
    try:
        urls = list(search(search_url, num_results=5))
        print("Found URLs:", urls)
        for i in urls:
            j = str(i)
            j = j.replace(".", "")
            j = j.replace("/", "")
            j = j.replace("-", "")
            j = j.lower()
            if domain in j and "mediabiasfactcheck" in j:
                url = i
                print(url)
                break
        else:
            return ["Unknown", "Unknown"]
        html = scrape_website_mbfc(url)
        if not html:
            return "Error while scraping"

        text = clean_body_content_mbfc(html)

        label_score = {
            "VERY HIGH": 10,
            "HIGH": 8,
            "MOSTLY FACTUAL": 6,
            "MIXED": 4,
            "LOW": 2,
            "VERY LOW": 1
        }
        ppol_stance = {
            "LEFT EXTREME":-7.5,
            "LEFT": -5,
            "LEFT-CENTER": -2.5,
            "LEAST BIASED": 0,
            "RIGHT-CENTER": 2.5,
            "RIGHT": 5,
            "RIGHT EXTREME": 7.5
        }
        for label, score in label_score.items():
            if f"Factual Reporting:\n{label}" in text:
                factual_score = score
                break
        else:
            factual_score = "Unknown"
        for stance, score in ppol_stance.items():
            if f"Bias Rating:\n{stance}" in text:
                ppol_stance = score
                break
        else:
            ppol_stance = "Unknown"

        return [factual_score, ppol_stance]
    except Exception as e:
        print(f"Error fetching MBFC score for {domain}: {e}")
        return ["Unknown", "Unknown"]
