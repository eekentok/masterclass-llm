# scripts/rag.py

#!/usr/bin/env python3

"""
rag.py

Amaç:
- Prompt oluştur
- Groq ChatCompletion ile yanıt üret
"""

from groq import Groq
from dotenv import load_dotenv
import os
import chromadb
from sentence_transformers import SentenceTransformer

load_dotenv()

GROQ_API_KEY = os.getenv("API_KEY")

client = Groq(api_key=GROQ_API_KEY)

# ChromaDB ve embedding modelini başlat
chroma_client = chromadb.PersistentClient(path="./data/chroma_db")
collection = chroma_client.get_or_create_collection("embedding_chunks")
embedding_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

def generate_answer(context, question):
    """
    TODO:
    - ChatCompletion çağrısı yap
    - prompt tasarla
    """

    system_prompt = (
        "Aşağıda sana verilen bilgi parçacıklarına dayanarak, kullanıcının sorusunu yanıtla. "
        "Eğer bilgi parçacıklarında cevap yoksa, 'Bu konuda elimde bilgi yok.' de.\n\n"
        "Tarzın: Nazik, anlaşılır ve profesyonel.\n"
        "Sınırların: Yorum yapma, yatırım tavsiyesi verme, finansal danışmanlık yapma.\n"
        "Gizlilik: Kimseden kişisel bilgileri sorma, kimseden kişisel bilgileri alma.\n"
        "Dil: Türkçe, eğer soru başka bir dildeyse, cevabını sorunun sorulduğu dilde ver.\n"
        "Bilgi parçacıkları:\n"
        f"{context}\n\n"
        f"Soru: {question}\nCevap:"
    )
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": "Sen Türkiye İş Bankası için tasarlanmış bir bankacılık asistanısın. Görevin sorulan bankacılık hizmetleri, ürünleri ve süreçleri hakkında sorulara elindeki bilgileri kullanarak cevap vermek."},
            {"role": "user", "content": system_prompt}
        ]
    )
    return response.choices[0].message.content.strip()

def main():
    question = input("Soru girin: ")
    # Sorgu embedding'i üret
    query_embedding = embedding_model.encode(question).tolist()
    # ChromaDB'den en yakın 3 chunk'ı çek
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=1,
        include=['documents']
    )
    # Chunk'ları birleştirip context oluştur
    context = "\n---\n".join(results['documents'][0])
    #print(context)
    answer = generate_answer(context, question)
    print("\nYanıt:")
    print(answer)

if __name__ == "__main__":
    main()
