# scripts/chunk.py

#!/usr/bin/env python3

"""
chunk.py

Amaç:
- Uzun metinleri belirli büyüklükte parçalara bölmek
"""

import pandas as pd

import pandas as pd

# Upload "scraped_data.csv"
df_scraped = pd.read_csv("data/scraped_data.csv")
scraped = df_scraped.to_dict(orient="records")
print(f"✅ {len(scraped)} içerik yüklendi.")


def chunk_text(text, max_length=500, overlap=50): # Used overlap so that at the end of the every chunk same words are used to provide context
# I tried with different chunk and overlape lengths(400/80 and 500/50), It did not affect the output quality
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = words[i:i+max_length]
        chunks.append(" ".join(chunk))
        i += max_length - overlap
    return chunks


# Merge the chunked texts inside "chunked_data", which looks like this [ {"url": "https://...", "title": "Mevduat", "chunk_id": 0, "text": "..."}, ....]
chunked_data = []

for entry in scraped:
    text = entry["content"]
    url = entry["url"]
    title = entry.get("title", "")

    chunks = chunk_text(text)
    for i, chunk in enumerate(chunks):
        chunked_data.append({
            "url": url,
            "title": title,
            "chunk_id": i,
            "text": chunk
        })


out_df = pd.DataFrame(chunked_data)
out_df.to_csv('data/chunked_data.csv', index=False)
print("✅ Chunk işlemi tamamlandı.")
