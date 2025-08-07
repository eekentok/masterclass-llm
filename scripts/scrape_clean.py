# scripts/scraper.py

#!/usr/bin/env python3

"""
scrape_clean.py

Amaç:
- Web scraping
- Sayfa başlığı, içerik ve URL'i almak
- Title almak için URL'den path kısmını kullanmak
- Datayı temizlemek ve düzenlemek.

"""

import trafilatura
import requests
import pandas as pd
import re
from urllib.parse import urlparse
from read_links import links

headers = {
    "User-Agent": "Mozilla/5.0"
}

def fetch_clean_text(url):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200: # 200 means success
            downloaded = trafilatura.extract(response.text) # Extracts the clean text.
            return downloaded
        else:
            print(f"[!] {url} status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"[X] Error fetching {url}: {e}")
        return None


def clean_text(text):
    if not text:
        return ""

    # Clean HTML tags
    text = re.sub(r'<[^>]+>', ' ', text)

    # Delete punctuations
    text = re.sub(r'[^\w\s]', ' ', text)

    # Lowercase
    text = text.lower()

    # Delete unnecessary spaces
    text = re.sub(r'\s+', ' ', text).strip()

    return text

def get_title_from_url(url): # Extract the title from the website.
    path = urlparse(url).path # Only takes the path part of the link
    return path.strip("/").split("/")[-1].replace("-", " ").replace("_", " ").title()


def main():
    scraped = []

    for i, link in enumerate(links):
        print(f"[{i+1}/{len(links)}] Fetching: {link}")
        text = clean_text(fetch_clean_text(link))
        if text: # If text is not empty.
            scraped.append({
                "url": link,
                "content": text,
                "title": get_title_from_url(link)
            })

    scraped_data = pd.DataFrame(scraped)
    scraped_data.to_csv('./data/scraped_data.csv', index=False)
    print("✅ Scraped data saved to scraped_data.csv")


if __name__ == "__main__":
    main()

