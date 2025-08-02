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

load_dotenv()

api_key = os.getenv("api_key")
client = Groq(api_key=api_key)

def generate_answer(context, question):
    """
    Call ChatCompletion.
    """
    prompt = f"""
Aşağıdaki bağlama (context) dayanarak kullanıcının sorusunu cevapla.

Soru: {question}

Bağlam:
{context}

Cevap:
"""
    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",  # veya llama3-8b-8192
            messages=[
                {"role": "system", "content": "Sen bir finans asistanısın. Soruları açık, anlaşılır ve bağlama dayalı olarak cevapla."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[!] Yanıt üretme hatası: {e}"

def main():
    """
    Bankacılık asistanı için interaktif komut satırı uygulaması.
    Her soruyu ayrı işlem olarak işler, geçmişi hatırlamaz.
    """
    import json
    from your_embedding_module import embed_query
    from search import search_context
    from rag import generate_answer

    # Upload embedding data
    with open("output/embeddings.jsonl", "r") as f:
        indexed_data = [json.loads(line) for line in f]

    while True:
        question = input("💬 Soru (çıkmak için -q): ").strip()
        if question.lower() in ["-q", "--quit", "çık", "exit"]:
            print("🔚 Çıkılıyor...")
            break

        # 1. Embed the question
        query_embedding = embed_query(question)

        # 2. Find closest contexts.
        top_context = search_context(query_embedding, indexed_data, k=5)

        # 3. Generate Answer
        answer = generate_answer(top_context, question)

        # 4. Answer
        print("\n📌 Yanıt:\n" + answer + "\n" + "-"*50)


if __name__ == "__main__":
    main()
