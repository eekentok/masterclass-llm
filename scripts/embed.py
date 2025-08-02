# scripts/embed.py

#!/usr/bin/env python3

"""
embed.py

Amaç:
- Groq Embedding API ile metni vektörleştir
- JSONL olarak kaydet
"""

import pandas as pd
import json
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("api_key")

client = Groq(api_key=api_key)

def embed_text(text):
    """
    Calling Groq Embedding API'yi turns the text into vectors.
    """
    try:
        response = client.embeddings.create(
            model="nomic-embed-text-v1", #llama3-70b-8192 or BAAI/bge-m3
            input=text
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"[!] Embedding hatası: {e}")
        return [0.0]*1536  


def main():
    df = pd.read_csv('../output/chunked_data.csv')
    with open('../output/embeddings.jsonl', 'w') as f:
        for idx, row in df.iterrows():
            embedding = embed_text(row['chunk'])
            record = {
                'url': row['url'],
                'title': row['title'],
                'chunk': row['chunk'],
                'embedding': embedding
            }
            f.write(json.dumps(record) + '\n')
    print("✅ Embedding tamamlandı.")

if __name__ == "__main__":
    main()
