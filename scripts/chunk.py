# scripts/chunk.py

#!/usr/bin/env python3

"""
chunk.py

Amaç:
- Uzun metinleri belirli büyüklükte parçalara bölmek
"""

import pandas as pd
from transformers import AutoTokenizer
import openai
from openai import OpenAI
from dotenv import load_dotenv
import os

#Get .env file
load_dotenv()

#Get API key from .env file
api_key = os.getenv("API_KEY")

#Create OpenAI client
client = OpenAI(api_key=api_key)

def chunk_text(text, size=100):
    """
    TODO:
    - text.split() ile kelimelere ayır
    - belirli büyüklükte parçala
    """
    return [text]  # Şu an parçalamıyor

def chunk_text_token_llama3(text, chunk_size=500, model_name="unsloth/llama-3-8b-bnb-4bit"):
    """
    Token-based chunking using HuggingFace's Llama 3 tokenizer.
    """
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokens = tokenizer.encode(str(text))
    chunks = [tokens[i:i+chunk_size] for i in range(0, len(tokens), chunk_size)]
    return [tokenizer.decode(chunk) for chunk in chunks]


def main():
    df = pd.read_csv('./data/cleaned_traf_data.csv')
    records = []

    for idx, row in df.iterrows():
        content = row['content']

        # A small print to see the title of the row that is being chunked
        title = row.get('title', f'Row {idx}')  # Eğer 'title' yoksa satır numarası kullan
        print(f"▶️ Chunking: {title}")
        
        chunks = chunk_text_token_llama3(content, chunk_size=500,)  # or another open tokenizer
        for chunk_id, chunk in enumerate(chunks):
            new_row = {
                'url': row['url'],
                'title': row['title'],
                'chunk': chunk,
                'chunk_id': chunk_id
            }
            records.append(new_row)

    out_df = pd.DataFrame(records)
    out_df.to_csv('./data/chunked_traf_data.csv', index=False)
    print("✅ Chunking completed. Output: chunked_traf_data.csv")
if __name__ == "__main__":
    main()
