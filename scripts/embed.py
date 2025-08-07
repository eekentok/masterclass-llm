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
from sentence_transformers import SentenceTransformer
import numpy as np

df_chunked = pd.read_csv("data/chunked_data.csv")
chunked_data = df_chunked.to_dict(orient="records")

load_dotenv()

api_key = os.getenv("API_KEY")  # .env dosyasından API anahtarını al
if not api_key:
    raise ValueError("API_KEY environment variable not set.")

client = Groq(api_key=api_key)

model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2") # Also tried with "paraphrase-multilingual-MiniLM-L12-v2" or "paraphrase-multilingual-mpnet-base-v2"

texts = [chunk["text"] for chunk in chunked_data]
embeddings = model.encode(texts, show_progress_bar=True)

# Merge all embeddings in a Numpy array. (all text in one matrix)
np.save("./data/embeddings.npy", embeddings)  # Save the embeddings to a file
print("✅ Embeddings saved to embeddings.npy")


embedding_array = np.array(embeddings).astype("float32") # FAISS only accepts float32 type arrays
# Save
np.save("./data/embedding_array.npy", embedding_array)
print("✅ Embedding array is saved to embedding_array.npy")