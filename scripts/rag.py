# scripts/rag.py

#!/usr/bin/env python3

"""
rag.py

Amaç:
- Prompt oluştur
- Groq ChatCompletion ile yanıt üret
"""


import faiss
import numpy as np
from dotenv import load_dotenv
import os
from groq import Groq
from search import search_context
import pandas as pd
from langdetect import detect


load_dotenv()

api_key = os.getenv("API_KEY")
client = Groq(api_key=api_key)

df = pd.read_csv("data/chunked_data.csv")
chunked_data = df.to_dict(orient="records")

def generate_answer(question):
    """
    Call ChatCompletion.
    """
    prompt = f"""
Sen finans, bankacılık ve ekonomi alanlarında uzmanlaşmış bir yapay zekâ danışmanısın.
Aşağıda bir kullanıcının sorusu ve bu soruya dair bazı bilgi parçaları (bağlam) yer alıyor. Görevin, bu bağlama dayanarak doğru, açık ve tekrar etmeyen bir cevap üretmek.
❗️ Cevabını hazırlarken şu kurallara dikkat et:
- Aynı kelimeleri tekrar tekrar kullanma. Anlamı koruyarak eş anlamlılarla zenginleştir.
- Gereksiz tekrarlar, döngüsel anlatımlar ve soyut genellemelerden kaçın.
- Uzunsa madde madde yaz.
- Elindeki bilgi yetersizse bunu dürüstçe belirt.
- Üst üste aynı kelimeleri kullanma.

### DİL ###
{detect(question)}

### BAĞLAM ###
{search_context(question)}

### SORU ###
{question}

### CEVAP ###
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4",  # veya llama3-8b-8192 veya llama3-70b-8192
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
    while True:
        question = input("💬 Soru (çıkmak için dur): ").strip()
        if question.lower() in ["q", "-quit", "çık", "exit", "dur", "du", "d"]:
            print("🔚 Çıkılıyor...")
            break

        answer = generate_answer(question)
        print("\n📌 Yanıt:\n" + answer + "\n" + "-"*50)


if __name__ == "__main__":
    main()