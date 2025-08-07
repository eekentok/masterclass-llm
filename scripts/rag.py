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
import json
import os
import chromadb
from sentence_transformers import SentenceTransformer
from langdetect import detect
import langcodes

def detect_language_name(text):
    lang_code = detect(text)
    try:
        return langcodes.get(lang_code).language_name()
    except:
        return f"Unknown ({lang_code})"



load_dotenv()

GROQ_API_KEY = os.getenv("API_KEY")

client = Groq(api_key=GROQ_API_KEY)

# ChromaDB ve embedding modelini başlat
chroma_client = chromadb.PersistentClient(path="./data/chroma_db")
collection = chroma_client.get_or_create_collection("embedding_chunks")
embedding_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

MAX_HISTORY = 10  # Sohbet geçmişinde tutulacak maksimum soru-cevap çifti

def generate_answer(context, question, chat_history=None, choose_model="llama3-70b-8192", language = "Turkish"):
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
        "- Respond in " + language + "\n"
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

def generate_chat_history(question, chat_history = []):
    """
    Girilen soruyu ve sohbet geçmişini kullanarak LLM için bir özet oluştur ve context oluştur.
    """
    sum_model = "llama3-8b-8192"  # Özetleme için kullanılacak model

    if chat_history is None:
        chat_history = []

    system_prompt = (
        "Use only the provided context information to generate your answer."
        "Rules:\n"
        "- Be helpful, kind, and concise.\n"
        "- If the answer is not in the provided context, say: 'Bu konuda elimde bilgi yok.'\n"
        "- Do not generate opinions, investment advice, or financial consulting.\n"
        "- Never ask for or store personal information.\n"
        "- Respond in " + language + "\n"
        "Provided context:\n"
        f"{context}\n\n"
        "User question: "
        f"{question}\nAnswer:"
    )

def choose_model():
    MODELS_FILE = "./data/models.json"

    if not os.path.exists(MODELS_FILE):
        print("Models file not found. Please add models to the data/models.json file.")
    else:
        with open(MODELS_FILE, "r") as f:
            models = json.load(f)
        
        print("Available models:")
        for model in models:
            print(f"{model['model_id']}: {model['model_title']} ({model['model_category']})")
        
        model_id = input("Select a model by ID: ")
        selected_model = next((m for m in models if str(m["model_id"]) == model_id), None)
        
        if selected_model:
            return selected_model["model_name"]
        else:
            print("Invalid model ID. Defaulting to 'llama3-70b-8192'.")
            return "llama3-70b-8192"

def main():
    chat_history = [
        {"role": "system", 
        "content": "Sen Türkiye İş Bankası için tasarlanmış bir bankacılık asistanısın. Görevin sorulan bankacılık hizmetleri, ürünleri ve süreçleri hakkında sorulara elindeki bilgileri kullanarak cevap vermek."}
    ]
    model = choose_model()

    while True:
        question = input("Soru girin: ")

        if question.strip() in ["-q", "--quit"]:
            print("Çıkılıyor...")
            break
        
        #Girilen promptun dilini ve dil kodunu algıla
        #lang_code = detect(question) #Gerekirse bu satırı dil kodunu algılamak için kullanabilirsiniz
        language = detect_language_name(question)
        #print(f"Algılanan dil: {language}")
        
        # Sorgu embedding'i üret
        query_embedding = embedding_model.encode(question).tolist()
        
        # ChromaDB'den en yakın 5 chunk'ı çek
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=15,
            include=['documents']
        )
        context = "\n---\n".join(results['documents'][0])
        
        # Sohbet geçmişinin son MAX_HISTORY*2 mesajını (soru-cevap) al
        trimmed_history = chat_history[-MAX_HISTORY*2:]
        
        # generate_answer fonksiyonunu kullan
        answer = generate_answer(context, question, trimmed_history, choose_model = model, language = language)
        print("\nYanıt:")
        print(answer + "\n--------------------------------")
        
        # Sohbet geçmişine ekle
        chat_history.append({"role": "user", "content": question})
        chat_history.append({"role": "assistant", "content": answer})

if __name__ == "__main__":
    main()
