# scripts/scraper.py

#!/usr/bin/env python3

"""
scraper.py

Amaç:
- Web scraping
- Sayfa başlığı, içerik ve URL'i almak
"""

import pandas as pd
import csv
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import trafilatura

def scrape_page(url):
    """
    TODO:
    - requests ile sayfayı çek
    - BeautifulSoup ile parse et
    - Başlık ve içerik çıkar
    """
       
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        downloaded = trafilatura.extract(response.text)
        print(downloaded)
    
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    # Başlık kontrolü: hem soup.title hem de soup.title.string var mı?
    if soup.title and soup.title.string:
        title = soup.title.string.strip()
    else:
        title = ''
    # İçerik olarak body'nin tamamını al
    content = soup.body.get_text(separator=' ', strip=True) if soup.body else ''
    return {"url": url, "title": title, "content": content}

def main():
    urls = []
    with open('combined_links.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row:  # Boş satırları atla
                urls.append(row[0])

    results = []
    for url in urls:
        if url[0:4] == 'http':
            print(f'Scraping {url}...')
            result = scrape_page(url)
            if result:
                results.append(result)

    df = pd.DataFrame(results)
    df.to_csv('scraped_data.csv', index=False)
    print("✅ Scraping tamamlandı.")

if __name__ == "__main__":
    main()
