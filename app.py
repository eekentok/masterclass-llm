#!/usr/bin/env python3

"""
Flask web application for the AI chatbot interface
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from groq import Groq
from dotenv import load_dotenv
import os
import chromadb
from sentence_transformers import SentenceTransformer
import json
from datetime import datetime

load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize Groq client
GROQ_API_KEY = os.getenv("API_KEY")
client = Groq(api_key=GROQ_API_KEY)

# Initialize ChromaDB and embedding model
chroma_client = chromadb.PersistentClient(path="./data/chroma_db")
collection = chroma_client.get_or_create_collection("embedding_chunks")
embedding_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

MAX_HISTORY = 10

def generate_answer(context, question, chat_history=None):
    """
    Generate answer using Groq ChatCompletion API
    """
    if chat_history is None:
        chat_history = []
    
    # Prepare messages for the API call
    messages = [
        {"role": "system", "content": "You are a polite, professional, and accurate AI assistant developed for Türkiye İş Bankası. Your task is to answer user questions about banking products, services, and procedures. Always respond in Turkish. If the answer is not in the provided context, say: 'Bu konuda elimde bilgi yok.' Do not generate opinions, investment advice, or financial consulting. Never ask for or store personal information. When providing lists, use proper HTML formatting: <ul><li>Item 1</li><li>Item 2</li></ul> for bullet lists or <ol><li>Item 1</li><li>Item 2</li></ol> for numbered lists."}
    ]
    
    # Add chat history if provided
    if chat_history:
        # Limit history to last MAX_HISTORY*2 messages
        trimmed_history = chat_history[-MAX_HISTORY*2:]
        messages.extend(trimmed_history)
    
    # Add current question with context (matching rag.py approach)
    user_message = f"{context}\n\nSoru: {question}\nCevap:"
    messages.append({"role": "user", "content": user_message})
    
    try:
        response = client.chat.completions.create(
            model=os.getenv("LLM_MODEL"),
            messages=messages
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Üzgünüm, bir hata oluştu: {str(e)}"

@app.route('/')
def index():
    """Render the main chat interface"""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat requests"""
    try:
        data = request.get_json()
        question = data.get('message', '').strip()
        chat_history = data.get('history', [])
        
        if not question:
            return jsonify({'error': 'Soru boş olamaz'}), 400
        
        # Generate query embedding
        query_embedding = embedding_model.encode(question).tolist()
        
        # Get relevant chunks from ChromaDB
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=10,
            include=['documents']
        )
        
        # Prepare context from retrieved documents
        context = "\n---\n".join(results['documents'][0]) if results['documents'][0] else ""
        
        # Generate answer
        answer = generate_answer(context, question, chat_history)
        
        # Prepare response
        response_data = {
            'answer': answer,
            'timestamp': datetime.now().isoformat(),
            'context_used': bool(context),
            'context_length': len(context)
        }
        
        return jsonify(response_data)
        
    except Exception as e:
        return jsonify({'error': f'Sunucu hatası: {str(e)}'}), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 