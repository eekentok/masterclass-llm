# scripts/search.py

#!/usr/bin/env python3

"""
search.py

Amaç:
- Kullanıcının sorusunu embed et
- En yakın chunk'ları bul ve göster
"""

import pandas as pd
import numpy as np
import json
from groq import Groq
from dotenv import load_dotenv
import os
import faiss
import numpy as np
import pickle
import openai
from embed import model
from transformers import AutoTokenizer


load_dotenv()
api_key = os.getenv("API_KEY")  # .env dosyasından API anahtarını al
client = Groq(api_key=api_key)

df_chunked = pd.read_csv("data/chunked_data.csv")
chunked_data = df_chunked.to_dict(orient="records")
embedding_array = np.load("data/embedding_array.npy").astype("float32") # load the embeddings from the file
embedding_dim = embedding_array.shape[1] #dimension of vector (size)
index = faiss.IndexFlatL2(embedding_dim) # create index
index.add(embedding_array) # add faiss indexes to array


metadata = [
    {
        "text": chunk["text"],
        "title": chunk.get("title", ""),
        "url": chunk["url"]
    }
    for chunk in chunked_data
] # create a metadata with all embeddings, titles, and faiss index


# write FAISS index in the file
faiss.write_index(index, "data/faiss_index.index")

# save Metadata with pickle
with open("data/faiss_metadata.pkl", "wb") as f:
    pickle.dump(metadata, f)

def search_context(query, k=5):
    query_embedding = model.encode([query]).astype("float32")
    D, I = index.search(query_embedding, k)
    from transformers import AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
    max_token_limit = 512 

    current_tokens = 0
    selected_chunks = []

    context_chunks = [metadata[i]["text"] for i in I[0]]


    for chunk in context_chunks:
        tokens = len(tokenizer.tokenize(chunk))
        if current_tokens + tokens > max_token_limit:
            break
        selected_chunks.append(chunk)
        current_tokens += tokens

    joined_context = "\n\n".join(selected_chunks)
    return joined_context
