# scripts/clean.py

#!/usr/bin/env python3

"""
clean.py

Amaç:
- HTML ve gereksiz karakterleri temizle
- Lower-case
"""

import pandas as pd

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def fetch_clean_text(url):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            downloaded = trafilatura.extract(response.text)
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
    # Clean punctuations
    text = re.sub(r'[^\w\s]', ' ', text)
    # Lowercase
    text = text.lower()
    # Clean unnecessary spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def main():
    df = pd.read_csv('../input/scraped_data.csv')
    df['cleaned_content'] = df['content'].apply(fetch_clean_text).apply(clean_text)
    df.to_csv('../output/cleaned_data.csv', index=False)
    print("✅ Temizleme tamamlandı.")

if __name__ == "__main__":
    main()
