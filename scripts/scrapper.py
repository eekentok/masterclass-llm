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

#Trafilatura version

def fetch_clean_text(url):

    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')
    # Başlık kontrolü: hem soup.title hem de soup.title.string var mı?
    if soup.title and soup.title.string:
        title = soup.title.string.strip()
    else:
        title = ''

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            content = trafilatura.extract(response.text)
            return {"url": url, "title": title, "content": content}
        else:
            print(f"[!] {url} status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"[X] Error fetching {url}: {e}")
        return None


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
    with open('./data/input/combined_links.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row and ".pdf" not in row[0].lower():  # Boş satırları ve .pdf içerenleri atla
                urls.append(row[0])

    results = []
    traf_text = []
    for url in urls:
        if url[0:4] == 'http':
            print(f'Scraping {url}...')
            #result = scrape_page(url)
            traf_res = fetch_clean_text(url)
            if traf_res:
                traf_text.append(traf_res)
            #if result:
            #    results.append(result)

    traf_df = pd.DataFrame(traf_text)
    traf_df.to_csv('./data/traf_data.csv', index = False)

    #df = pd.DataFrame(results)
    #df.to_csv('scraped_data.csv', index=False)
    print("✅ Scraping tamamlandı.")

if __name__ == "__main__":
    main()
