# scripts/rag.py

#!/usr/bin/env python3

"""
rag.py

Amaç:
- Prompt oluştur
- Groq ChatCompletion ile yanıt üret
- RAG-based chat history kullan (RAM-based)
"""

from groq import Groq
from dotenv import load_dotenv
import os
import chromadb
from sentence_transformers import SentenceTransformer
import json
import uuid
from datetime import datetime
import numpy as np
from typing import List, Dict, Tuple, Optional

load_dotenv()

GROQ_API_KEY = os.getenv("API_KEY")

client = Groq(api_key=GROQ_API_KEY)

# ChromaDB ve embedding modelini başlat
chroma_client = chromadb.PersistentClient(path="./data/chroma_db")
collection = chroma_client.get_or_create_collection("embedding_chunks")
embedding_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

# RAM-based chat history storage
class RAMChatHistory:
    def __init__(self):
        self.conversations: List[Dict] = []
        self.embeddings: List[List[float]] = []
        self.session_embeddings: Dict[str, List[int]] = {}  # session_id -> conversation indices
    
    def store_conversation_turn(self, question: str, answer: str, session_id: Optional[str] = None) -> str:
        """
        Soru-cevap çiftini RAM'de sakla
        """
        if session_id is None:
            session_id = str(uuid.uuid4())
        
        # Soru ve cevabı birleştir
        conversation_text = f"Soru: {question}\nCevap: {answer}"
        
        # Embedding oluştur
        embedding = embedding_model.encode(conversation_text).tolist()
        
        # Metadata hazırla
        metadata = {
            "session_id": session_id,
            "timestamp": datetime.now().isoformat(),
            "question": question,
            "answer": answer,
            "type": "conversation"
        }
        
        # RAM'e kaydet
        conversation_data = {
            "text": conversation_text,
            "metadata": metadata,
            "embedding": embedding
        }
        
        self.conversations.append(conversation_data)
        self.embeddings.append(embedding)
        
        # Session mapping'i güncelle
        if session_id not in self.session_embeddings:
            self.session_embeddings[session_id] = []
        self.session_embeddings[session_id].append(len(self.conversations) - 1)
        
        return session_id
    
    def retrieve_relevant_history(self, current_question: str, session_id: Optional[str] = None, top_k: int = 5) -> Tuple[List[str], List[Dict]]:
        """
        Mevcut soruya en yakın geçmiş konuşmaları getir
        """
        if not self.conversations:
            return [], []
        
        # Mevcut sorunun embedding'ini oluştur
        question_embedding = embedding_model.encode(current_question).tolist()
        
        # Tüm konuşmalarla benzerlik hesapla
        similarities = []
        for i, stored_embedding in enumerate(self.embeddings):
            similarity = self._cosine_similarity(question_embedding, stored_embedding)
            similarities.append((similarity, i))
        
        # Benzerliklere göre sırala
        similarities.sort(reverse=True)
        
        # Session'a ait konuşmaları önceliklendir
        if session_id and session_id in self.session_embeddings:
            session_indices = set(self.session_embeddings[session_id])
            
            # Session konuşmalarını önceliklendir
            session_similarities = [(sim, idx) for sim, idx in similarities if idx in session_indices]
            other_similarities = [(sim, idx) for sim, idx in similarities if idx not in session_indices]
            
            # Session konuşmalarını önce ekle, sonra diğerlerini ekle
            selected_indices = [idx for _, idx in session_similarities[:top_k//2]]
            remaining_count = top_k - len(selected_indices)
            selected_indices.extend([idx for _, idx in other_similarities[:remaining_count]])
        else:
            selected_indices = [idx for _, idx in similarities[:top_k]]
        
        # Seçilen konuşmaları getir
        relevant_conversations = [self.conversations[idx]["text"] for idx in selected_indices]
        relevant_metadatas = [self.conversations[idx]["metadata"] for idx in selected_indices]
        
        return relevant_conversations, relevant_metadatas
    
    def _cosine_similarity(self, a: List[float], b: List[float]) -> float:
        """
        İki vektör arasındaki cosine similarity hesapla
        """
        a = np.array(a)
        b = np.array(b)
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    
    def get_session_conversations(self, session_id: str) -> List[Dict]:
        """
        Belirli bir session'a ait tüm konuşmaları getir
        """
        if session_id not in self.session_embeddings:
            return []
        
        session_indices = self.session_embeddings[session_id]
        return [self.conversations[idx] for idx in session_indices]
    
    def clear_session(self, session_id: str):
        """
        Belirli bir session'ı temizle
        """
        if session_id in self.session_embeddings:
            del self.session_embeddings[session_id]

# Global chat history instance
chat_history = RAMChatHistory()

def store_conversation_turn(question: str, answer: str, session_id: Optional[str] = None) -> str:
    """
    Soru-cevap çiftini RAM'de sakla
    """
    return chat_history.store_conversation_turn(question, answer, session_id)

def retrieve_relevant_history(current_question: str, session_id: Optional[str] = None, top_k: int = 5) -> Tuple[List[str], List[Dict]]:
    """
    Mevcut soruya en yakın geçmiş konuşmaları getir
    """
    return chat_history.retrieve_relevant_history(current_question, session_id, top_k)

def format_chat_history_for_prompt(relevant_conversations: List[str], metadatas: List[Dict]) -> str:
    """
    İlgili konuşma geçmişini prompt için formatla
    """
    if not relevant_conversations:
        return ""
    
    history_text = "Önceki ilgili konuşmalar:\n"
    for i, (conv, metadata) in enumerate(zip(relevant_conversations, metadatas)):
        history_text += f"{i+1}. {conv}\n"
    
    return history_text

def generate_answer(context: str, question: str, chat_history_data: Optional[List] = None) -> str:
    """
    TODO:
    - ChatCompletion çağrısı yap
    - prompt tasarla
    """
    
    if chat_history_data is None:
        chat_history_data = []

    # İlgili konuşma geçmişini al
    relevant_conversations, metadatas = retrieve_relevant_history(question)
    history_context = format_chat_history_for_prompt(relevant_conversations, metadatas)

    system_prompt = (
        "Use only the provided context information to generate your answer."
        "Rules:\n"
        "- Be kind, helpful, and concise.\n"
        "- If the answer is not in the provided context, say: 'Bu konuda elimde bilgi yok.'\n"
        "- Do not generate opinions, investment advice, or financial consulting.\n"
        "- Never ask for or store personal information.\n"
        "- Always respond in Turkish.\n"
        "- If the user asks a question in another language, answer in that language using English-generated content translated to the user's language.\n"
        "- Consider previous relevant conversations when answering.\n"
        "Provided context:\n"
        f"{context}\n\n"
        f"{history_context}\n\n"
        "User question: "
        f"{question}\nAnswer:"
    )
    
    # Chat history'yi kullan (sadece system prompt ile)
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": question}
    ]
    
    response = client.chat.completions.create(
        model=os.getenv("LLM_MODEL"),
        messages=messages
    )
    return response.choices[0].message.content.strip()

def main():
    session_id = str(uuid.uuid4())  # Yeni session başlat
    
    while True:
        question = input("Soru girin: ")
        if question.strip() in ["-q", "--quit"]:
            print("Çıkılıyor...")
            break
            
        # Sorgu embedding'i üret
        query_embedding = embedding_model.encode(question).tolist()
        
        # ChromaDB'den en yakın 5 chunk'ı çek
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=10,
            include=['documents']
        )
        context = "\n---\n".join(results['documents'][0])
        
        # RAG-based chat history ile yanıt üret
        answer = generate_answer(context, question)
        print("\nYanıt:")
        print(answer + "\n--------------------------------")
        
        # Konuşmayı RAM'e kaydet
        store_conversation_turn(question, answer, session_id)

if __name__ == "__main__":
    main()
