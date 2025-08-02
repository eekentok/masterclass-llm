# scripts/search.py

#!/usr/bin/env python3

"""
search.py

Amaç:
- Kullanıcının sorusunu embed et
- En yakın chunk'ları bul ve göster
"""

import numpy as np
import json
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("api_key")
client = Groq(api_key=api_key)

def cosine_similarity(a, b):
    """Calculates the similarity between two vectors"""
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def embed_query(text):
    """Turn the question into embeddings"""
    try:
        response = client.embeddings.create(
            model="nomic-embed-text-v1",
            input=text
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"[!] Embed hatası: {e}")
        return None

def main():
    query = input("❓Sorunuzu girin:")
    query_embedding = embed_query(query)
    if query_embedding is None:
        return

    records = []
    with open("../output/embeddings.jsonl", "r") as f:
        for line in f:
            records.append(json.loads(line))

    # Calcualte similarities between all records
    scored = []
    for record in records:
        score = cosine_similarity(query_embedding, record["embedding"])
        scored.append((score, record))

    # En yüksek skorlu 3 chunk'ı getir
    top_k = sorted(scored, key=lambda x: x[0], reverse=True)[:3]

    print("\n📚 En yakın içerikler:")
    for i, (score, record) in enumerate(top_k, 1):
        print(f"\n#{i} | Skor: {score:.3f}")
        print(f"Başlık: {record['title']}")
        print(f"Kaynak: {record['url']}")
        print(f"Metin: {record['chunk'][:300]}...")  # İlk 300 karakter

if __name__ == "__main__":
    main()
