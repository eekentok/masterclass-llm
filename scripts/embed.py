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
from sentence_transformers import SentenceTransformer

#Get .env file
load_dotenv()

#Get API key from .env file
GROQ_API_KEY = os.getenv("API_KEY")

#Create Groq client
client = Groq(api_key=GROQ_API_KEY)

# Modeli bir kez yükle (çok dilli, hızlı ve hafif bir model)
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

def embed_text(text):
    
    """
    TODO:
    - Groq Embedding API çağır
    - Model adını belirle
    """
    
    try:
        embedding = model.encode(text)
        return embedding.tolist()  # JSON'a yazmak için listeye çeviriyoruz
    except Exception as e:
        print(f"Embedding hatası: {e}")
        return None

def main():
    df = pd.read_csv('./data/chunked_traf_data.csv')
    with open('./data/output/embeddings.jsonl', 'w') as f:
        for idx, row in df.iterrows():

            print(f"Processing row {idx+1} of {len(df)}")
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