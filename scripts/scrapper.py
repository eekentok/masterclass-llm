# scripts/scraper.py

#!/usr/bin/env python3

"""
scraper.py

Amaç:
- Web scraping
- Sayfa başlığı, içerik ve URL'i almak
"""

import pandas as pd
import requests
import trafilatura

headers = {
    "User-Agent": "Mozilla/5.0"
}

def scrape_page(url):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"[!] {url} → Status code: {response.status_code}")
            return None

        # fetch content with Trafilatura from HTML
        downloaded = trafilatura.extract(response.text)
        if not downloaded:
            print(f"[!] Trafılatura içerik bulamadı: {url}")
            return None

        return {
            "url": url,
            "title": url.split("/")[-1].replace("-", " ").title(),
            "content": downloaded
        }

    except Exception as e:
        print(f"[X] Hata ({url}): {e}")
        return None

def main():
    df = pd.read_csv("../input/links11.csv", header=None)
    urls = df[0].dropna().unique().tolist()
    urls = [url for url in urls if not url.lower().endswith(".pdf")]

    results = []
    for i, url in enumerate(urls):
        print(f"[{i+1}/{len(urls)}] Fetching: {url}")
        result = scrape_page(url)
        if result:
            results.append(result)

    df_scraped = pd.DataFrame(results)
    df_scraped.to_csv("../input/scraped_data.csv", index=False)
    print("✅ Scraping tamamlandı.")

if __name__ == "__main__":
    main()

