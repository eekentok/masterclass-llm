# scripts/chunk.py

#!/usr/bin/env python3

"""
chunk.py

Amaç:
- Uzun metinleri belirli büyüklükte parçalara bölmek
"""

import pandas as pd

def chunk_text(text, max_length=500, overlap=50): #used overlap so that at the end of the every chunk same words are used to provide context
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = words[i:i+max_length]
        chunks.append(" ".join(chunk))
        i += max_length - overlap
    return chunks


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
    out_df.to_csv('../output/chunked_data.csv', index=False)
    print("✅ Chunk işlemi tamamlandı.")

if __name__ == "__main__":
    main()
