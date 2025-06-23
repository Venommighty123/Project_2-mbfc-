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
from scraper import clean_body_content, scrape_website
from mbfc_scraper import scrape_website_mbfc, clean_body_content_mbfc, fetch_mbfc_factual_score
from web_chunker import clean_html, remove_boilerplate_lines, trim_head_tail, paragraph_based_chunking
import nltk
from nltk.tokenize import sent_tokenize

def process_claim(claim, num_sites=20):
    results = []
    print(f"\n🔎 Searching for claim: {claim}")
    query = f"{claim} site:news"
    urls_scraped = list(search(claim, num_results=num_sites))
    print(urls_scraped)
    urls = []
    for url in urls_scraped:
        if len(urls) > 10:
            break
        if "youtube" in str(url) or len(str(url)) < 15:
            continue
        else:
            urls.append(url)
    print(urls)
    nltk.download('punkt_tab')

    for url in urls:
        print(f"🌐 Analyzing: {url}")
        html = scrape_website(url)
        if not html:
            continue
        text = clean_html(html)
        text = remove_boilerplate_lines(text)
        text = trim_head_tail(text)
        text = text.replace("\"", "")
        text = text.replace("\'", "")
        sentences = sent_tokenize(text)
        chunks = paragraph_based_chunking(sentences)
        # dom_content = clean_body_content(html)
        # stance = get_nli_stance(claim, dom_content)
        domain = urlparse(url).netloc
        scores = fetch_mbfc_factual_score(domain)
        for substr in [".", "/", "-", "www", "org", "en", "com"]:
            domain = domain.replace(substr, "")
        stance = scores[1]
        credibility_score = scores[0]
        results.append({
            "url": url,
            "domain": domain,
            "stance": stance,
            "credibility_score": credibility_score,
            "claims": chunks
        })

    # Save to CSV
    with open("claim_analysis_4.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["url", "domain", "stance", "credibility_score", "claims"])
        writer.writeheader()
        writer.writerows(results)

    print("\n✅ Results saved to claim_analysis.csv")
    return results

# Run
if __name__ == "__main__":
    input_claim = input("Enter the claim to verify: ")
    process_claim(input_claim)