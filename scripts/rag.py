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

MAX_HISTORY = 10  # Sohbet geçmişinde tutulacak maksimum soru-cevap çifti

def generate_answer(context, question, chat_history=None, choose_model="llama3-70b-8192"):
    """
    TODO:
    - ChatCompletion çağrısı yap
    - prompt tasarla
    """
    
    if chat_history is None:
        chat_history = []

    system_prompt = (
        "Use only the provided context information to generate your answer."
        "Rules:\n"
        "- Be helpful, kind, and concise.\n"
        "- If the answer is not in the provided context, say: 'Bu konuda elimde bilgi yok.'\n"
        "- Do not generate opinions, investment advice, or financial consulting.\n"
        "- Never ask for or store personal information.\n"
        "- Always respond in Turkish.\n"
        "- If the user asks a question in another language, answer in that language using English-generated content translated to the user's language.\n"
        "Provided context:\n"
        f"{context}\n\n"
        "User question: "
        f"{question}\nAnswer:"
    )
    
    # Chat history'yi kullan
    messages = chat_history + [
        {"role": "user",
        "content": system_prompt}
    ]
    
    response = client.chat.completions.create(
        model=choose_model,
        messages=messages
    )
    return response.choices[0].message.content.strip()

def main():
    chat_history = [
        {"role": "system", "content": "You are a polite, professional, and accurate AI assistant developed for Türkiye İş Bankası. Your task is to answer user questions about banking products, services, and procedures."}
    ]
    choose_model = input("1.LLama 3 70B (Daha kısa cevaplar)\n2.Qwen 3(Daha uzun cevaplar)\nDevam etmek için model seçin, 1 veya 2 yazın: ")
    if choose_model == "" or choose_model == "1":
        choose_model = "llama3-70b-8192"
    elif choose_model == "2":
        choose_model = "Qwen/Qwen3-32B"
    else:
        print("Geçerli bir model seçilmedi, LLama 3 70B seçiliyor.\n")
        choose_model = "llama3-70b-8192"
    print(f"Model: {choose_model}\n")
    
    while True:
        question = input("Soru girin: ")
        if question.strip() in ["-q", "--quit"]:
            print("Çıkılıyor...")
            break
        # Sorgu embedding'i üret
        query_embedding = embedding_model.encode(question).tolist()
        # ChromaDB'den en yakın x chunk'ı çek
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=15,
            include=['documents']
        )
        context = "\n---\n".join(results['documents'][0])
        # Sohbet geçmişinin son MAX_HISTORY*2 mesajını (soru-cevap) al
        trimmed_history = chat_history[-MAX_HISTORY*2:]
        # generate_answer fonksiyonunu kullan
        answer = generate_answer(context, question, trimmed_history, choose_model = choose_model)
        print("\nYanıt:")
        print(answer + "\n--------------------------------")
        # Sohbet geçmişine ekle
        chat_history.append({"role": "user", "content": question})
        chat_history.append({"role": "assistant", "content": answer})

if __name__ == "__main__":
    main()
