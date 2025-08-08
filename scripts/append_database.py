#!/usr/bin/env python3

"""
append_database.py

Amaç:
- new_links.csv dosyasını oku
- URL'leri scrape et (scrapper.py fonksiyonları kullanarak)
- clean.py, chunk.py, embed.py ve chroma_ingest.py pipeline'ını uygula
- Yeni CSV dosyalarını data/appender klasörüne kaydet
- Embedding'leri data/output/append_embeddings.jsonl olarak kaydet
- ChromaDB'ye yeni verileri ekle
"""

import pandas as pd
import os
import json
import chromadb
from chromadb.config import Settings
import csv
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import trafilatura

# Import functions from existing scripts
import sys
sys.path.append('.')

from scripts.clean import clean_navigation_text, replaceSpecialChars, str_basicclean
from scripts.chunk import split_sentences  # Import the sentence splitter
from transformers import AutoTokenizer     # Import tokenizer for chunking
from scripts.embed import embed_text

def fetch_clean_text(url):
    """
    Scrape and extract clean text from URL using trafilatura
    """
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Başlık kontrolü: hem soup.title hem de soup.title.string var mı?
            if soup.title and soup.title.string:
                title = soup.title.string.strip()
            else:
                title = ''
            
            content = trafilatura.extract(response.text)
            return {"url": url, "title": title, "content": content}
        else:
            print(f"[!] {url} status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"[X] Error fetching {url}: {e}")
        return None

def scrape_urls_from_csv(csv_file_path):
    """
    Scrape URLs from CSV file and return DataFrame with scraped content
    """
    print("🌐 Scraping URLs from new_links.csv...")
    
    urls = []
    with open(csv_file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row and ".pdf" not in row[0].lower():  # Boş satırları ve .pdf içerenleri atla
                urls.append(row[0])

    results = []
    for url in urls:
        if url[0:4] == 'http':
            print(f'Scraping {url}...')
            result = fetch_clean_text(url)
            if result:
                results.append(result)

    df = pd.DataFrame(results)
    print(f"✅ Scraped {len(df)} URLs successfully")
    return df

def clean_data(df):
    """
    Clean the data using the same logic as clean.py
    """
    print("🧹 Cleaning data...")
    
    # Apply basic cleaning
    str_basicclean(df, 'content', 'low')
    
    # Clean navigation text
    print("Navigasyon metinleri temizliği başlıyor...")
    df['content'] = df['content'].fillna('')
    df['content'] = df['content'].apply(clean_navigation_text)
    
    return df

def sentence_split_data(df):
    """
    Split the data into sentences and save as a DataFrame.
    """
    print("✂️ Splitting data into sentences...")
    records = []
    for idx, row in df.iterrows():
        content = row['content']
        title = row.get('title', f'Row {idx}')
        url = row['url']
        sentences = split_sentences(content)
        for sent_id, sentence in enumerate(sentences):
            records.append({
                'url': url,
                'title': title,
                'sentence': sentence,
                'sentence_id': sent_id
            })
    return pd.DataFrame(records)

def chunk_sentences(df, chunk_size=500, model_name="unsloth/llama-3-8b-bnb-4bit"):
    """
    Tokenize and chunk sentences without splitting sentences or words.
    """
    print("✂️ Chunking sentences into token-based chunks...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    records = []
    current_chunk = []
    current_tokens = 0
    chunk_id = 0
    prev_url = None
    prev_title = None

    for idx, row in df.iterrows():
        sentence = row['sentence']
        url = row['url']
        title = row['title']
        sentence_tokens = len(tokenizer.encode(sentence, add_special_tokens=False))

        # If new document, flush current chunk
        if prev_url is not None and url != prev_url:
            if current_chunk:
                records.append({
                    'url': prev_url,
                    'title': prev_title,
                    'chunk': " ".join(current_chunk),
                    'chunk_id': chunk_id
                })
                chunk_id = 0
                current_chunk = []
                current_tokens = 0

        if current_tokens + sentence_tokens > chunk_size:
            if current_chunk:
                records.append({
                    'url': url,
                    'title': title,
                    'chunk': " ".join(current_chunk),
                    'chunk_id': chunk_id
                })
                chunk_id += 1
            current_chunk = [sentence]
            current_tokens = sentence_tokens
        else:
            current_chunk.append(sentence)
            current_tokens += sentence_tokens

        prev_url = url
        prev_title = title

    # Add last chunk
    if current_chunk:
        records.append({
            'url': prev_url,
            'title': prev_title,
            'chunk': " ".join(current_chunk),
            'chunk_id': chunk_id
        })

    return pd.DataFrame(records)

def embed_data(df):
    """
    Embed the data using the same logic as embed.py
    """
    print("🔢 Creating embeddings...")
    embeddings_data = []
    
    for idx, row in df.iterrows():
        print(f"Processing row {idx+1} of {len(df)}")
        embedding = embed_text(row['chunk'])
        record = {
            'url': row['url'],
            'title': row['title'],
            'chunk': row['chunk'],
            'embedding': embedding
        }
        embeddings_data.append(record)
    
    return embeddings_data

def append_to_chroma(embeddings_data):
    """
    Append embeddings to ChromaDB using the same logic as chroma_ingest.py
    """
    print("🗄️ Appending to ChromaDB...")
    
    # ChromaDB client'ı başlat (local, varsayılan ayarlarla)
    client = chromadb.PersistentClient(path="./data/chroma_db")

    # Koleksiyon oluştur veya var olanı al
    collection = client.get_or_create_collection("embedding_chunks")

    # Embedding ve metadata'ları hazırla
    embeddings = []
    metadatas = []
    documents = []
    ids = []

    # Mevcut ID'leri al
    existing_ids = set()
    try:
        existing_data = collection.get()
        if existing_data['ids']:
            existing_ids = set(existing_data['ids'])
    except:
        pass

    # Yeni ID'ler oluştur
    start_id = len(existing_ids)
    
    for idx, record in enumerate(embeddings_data):
        print(f"{idx+1}. embedding ve metadata ChromaDB üzerine işleniyor...")
        embeddings.append(record['embedding'])
        metadatas.append({
            'url': record['url'],
            'title': record['title']
        })
        documents.append(record['chunk'])
        ids.append(str(start_id + idx))  # Her kayda benzersiz bir id

    # ChromaDB'ye ekle
    collection.add(
        embeddings=embeddings,
        metadatas=metadatas,
        documents=documents,
        ids=ids
    )

    print(f"✅ {len(embeddings)} embedding ChromaDB'ye eklendi.")

def main():
    print("🚀 Starting append database pipeline...")
    
    # Ensure directories exist
    os.makedirs('./data/appender', exist_ok=True)
    os.makedirs('./data/output', exist_ok=True)
    
    # Step 0: Scrape URLs from new_links.csv
    df_scraped = scrape_urls_from_csv("./data/input/new_links.csv")
    df_scraped.to_csv('./data/appender/scraped_new_data.csv', index=False)
    print("✅ Scraped data saved to data/appender/scraped_new_data.csv")
    
    # Step 1: Clean data
    df_cleaned = clean_data(df_scraped)
    df_cleaned.to_csv('./data/appender/cleaned_new_data.csv', index=False)
    print("✅ Cleaned data saved to data/appender/cleaned_new_data.csv")
    
    # Step 2: Sentence split
    df_sentences = sentence_split_data(df_cleaned)
    df_sentences.to_csv('./data/appender/sentence_split_new_data.csv', index=False)
    print("✅ Sentence split data saved to data/appender/sentence_split_new_data.csv")
    
    # Step 3: Chunk sentences
    df_chunked = chunk_sentences(df_sentences, chunk_size=500)
    df_chunked.to_csv('./data/appender/chunked_new_data.csv', index=False)
    print("✅ Chunked data saved to data/appender/chunked_new_data.csv")
    
    # Step 4: Create embeddings
    embeddings_data = embed_data(df_chunked)

    # Save embeddings to JSONL
    with open('./data/output/append_embeddings.jsonl', 'w') as f:
        for record in embeddings_data:
            f.write(json.dumps(record) + '\n')
    print("✅ Embeddings saved to data/output/append_embeddings.jsonl")
    
    # Step 5: Append to ChromaDB
    append_to_chroma(embeddings_data)
    
    print("🎉 Append database pipeline completed successfully!")

if __name__ == "__main__":
    main()