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

def chunk_text_token_llama3(text, chunk_size=8192, model_name="unsloth/llama-3-8b-bnb-4bit"):
    """
    Token-based chunking using HuggingFace's Llama 3 tokenizer.
    NOTE: If Groq's official tokenizer is not available on HuggingFace, we use Meta's Llama 3 tokenizer as a close equivalent for tokenization/chunking.
    """
    # If Groq releases an official tokenizer, replace the model_name below with the correct one, e.g.:
    # model_name="TheBloke/Groq-Llama-3-70B-base-GGUF"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokens = tokenizer.encode(str(text))
    chunks = [tokens[i:i+chunk_size] for i in range(0, len(tokens), chunk_size)]
    return [tokenizer.decode(chunk) for chunk in chunks]


def query_groq_llama3_70b(api_key, prompt, system_prompt="You are a helpful assistant for a bank."):
    # TODO: The 'openai.api_base' option isn't read in the client API. You will need to pass it when you instantiate the client, e.g. 'OpenAI(base_url="https://api.groq.com/openai/v1")'
    # openai.api_base = "https://api.groq.com/openai/v1"
    response = client.chat.completions.create(model="llama3-70b-8192",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ])
    return response.choices[0].message.content


def main():
    df = pd.read_csv('cleaned_traf_data.csv')
    records = []

    for idx, row in df.iterrows():
        content = row['content']
        chunks = chunk_text_token_llama3(content, chunk_size=8192, model_name="unsloth/llama-3-8b-bnb-4bit")  # or another open tokenizer
        for chunk_id, chunk in enumerate(chunks):
            new_row = row.copy()
            new_row['content'] = chunk
            new_row['chunk_id'] = chunk_id
            records.append(new_row)

    out_df = pd.DataFrame(records)
    out_df.to_csv('chunked_traf_data.csv', index=False)
    print("✅ Chunking completed. Output: chunked_traf_data.csv")
if __name__ == "__main__":
    main()
