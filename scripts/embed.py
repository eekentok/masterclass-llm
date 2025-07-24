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
from groq import Groq
from dotenv import load_dotenv
import os

#Get .env file
load_dotenv()

#Get API key from .env file
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

#Create Groq client
client = Groq(api_key=GROQ_API_KEY)

def embed_text(text):
    """
    TODO:
    - Groq Embedding API çağır
    - Model adını belirle
    """
    return [0.0]*1536  # Dummy örnek vektör

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
