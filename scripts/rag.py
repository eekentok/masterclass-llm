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
    question = "Vadeli mevduat nedir?"
    context = """
Vadeli Mevduat, belirli bir vade süresi boyunca bankaya yatırılan para karşılığında faiz geliri elde edilmesini sağlayan bir tasarruf aracıdır. Vade dolmadan çekilirse faiz hakkı kaybedilebilir. Genellikle düşük riskli yatırım olarak görülür.
"""
    answer = generate_answer(context, question)
    print("\n🧠 Yanıt:")
    print(answer)

if __name__ == "__main__":
    main()
