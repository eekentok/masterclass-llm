# scripts/chunk.py

#!/usr/bin/env python3

"""
chunk.py

Amaç:
- Uzun metinleri belirli büyüklükte parçalara bölmek
"""

import pandas as pd
from transformers import AutoTokenizer
import os
import langcodes
from langdetect import detect
import stanza
import spacy_stanza

# İlk indirmeleri yap
#stanza.download("en")
#stanza.download("tr")

# Pipelineleri yükle
nlp_tr = spacy_stanza.load_pipeline("tr")
nlp_en = spacy_stanza.load_pipeline("en")

# Metni cümlelere ayır
def split_sentences(text):
    lang = detect(text)
    if lang == "tr":
        doc = nlp_tr(text)
    elif lang == "en":
        doc = nlp_en(text)
    else:
        # Varsayılan olarak Türkçeyi dene
        doc = nlp_tr(text)

    return [sent.text.strip() for sent in doc.sents]

def chunk_text_token_llama3(text, chunk_size=500, model_name="unsloth/llama-3-8b-bnb-4bit"):
    """
    Sentence-aware token-based chunking using HuggingFace's Llama 3 tokenizer.
    Sentences are not split across chunks.
    """
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    sentences = split_sentences(text)
    chunks = []
    current_chunk = ""
    current_tokens = 0

    for sentence in sentences:
        sentence_tokens = len(tokenizer.encode(sentence, add_special_tokens=False))
        # If adding this sentence would exceed the chunk size, start a new chunk
        if current_tokens + sentence_tokens > chunk_size:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence
            current_tokens = sentence_tokens
        else:
            if current_chunk:
                current_chunk += " " + sentence
            else:
                current_chunk = sentence
            current_tokens += sentence_tokens

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


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
    out_df.to_csv('./data/new_chunked_traf_data.csv', index=False)
    print("✅ Chunking completed. Output: chunked_traf_data.csv")
if __name__ == "__main__":
    main()
