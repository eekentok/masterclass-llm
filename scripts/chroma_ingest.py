import chromadb
from chromadb.config import Settings
import json
import os

def main():
    # ChromaDB client'ı başlat (local, varsayılan ayarlarla)
    client = chromadb.PersistentClient(path="./chroma_db")

    # Koleksiyon oluştur veya var olanı al
    collection = client.get_or_create_collection("embedding_chunks")

    # Embedding ve metadata'ları oku
    embeddings = []
    metadatas = []
    documents = []
    ids = []

    with open('./data/output/embeddings.jsonl', 'r') as f:
        for idx, line in enumerate(f):
            record = json.loads(line)
            print(f"{idx+1}. embedding ve metadata ChromaDB üzerine işleniyor...")
            embeddings.append(record['embedding'])
            metadatas.append({
                'url': record['url'],
                'title': record['title']
            })
            documents.append(record['chunk'])
            ids.append(str(idx))  # Her kayda benzersiz bir id

    # ChromaDB'ye ekle
    collection.add(
        embeddings=embeddings,
        metadatas=metadatas,
        documents=documents,
        ids=ids
    )

    print(f"✅ {len(embeddings)} embedding ChromaDB'ye yüklendi.")
    print("Klasörler:", os.listdir("."))
if __name__ == "__main__":
    main()