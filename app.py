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

# Available models
AVAILABLE_MODELS = {
    "llama3-70b-8192": "Llama 3 70B (Daha kısa cevaplar)",
    "Qwen/Qwen3-32B": "Qwen 3 (Daha uzun cevaplar)"
}

def generate_answer(context, question, chat_history=None, choose_model="llama3-70b-8192"):
    """
    Generate answer using Groq ChatCompletion API with model selection
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
    
    try:
        response = client.chat.completions.create(
            model=choose_model,
            messages=messages
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Üzgünüm, bir hata oluştu: {str(e)}"

@app.route('/')
def index():
    """Render the main chat interface"""
    return render_template('index.html', models=AVAILABLE_MODELS)

@app.route('/api/models')
def get_models():
    """Get available models"""
    return jsonify({
        'models': AVAILABLE_MODELS,
        'default_model': 'llama3-70b-8192'
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat requests"""
    try:
        data = request.get_json()
        question = data.get('message', '').strip()
        chat_history = data.get('history', [])
        selected_model = data.get('model', 'llama3-70b-8192')
        
        if not question:
            return jsonify({'error': 'Soru boş olamaz'}), 400
        
        # Validate model selection
        if selected_model not in AVAILABLE_MODELS:
            selected_model = 'llama3-70b-8192'
        
        # Generate query embedding
        query_embedding = embedding_model.encode(question).tolist()
        
        # Get relevant chunks from ChromaDB
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=15,  # Increased from 10 to match rag.py
            include=['documents']
        )
        
        # Prepare context from retrieved documents
        context = "\n---\n".join(results['documents'][0]) if results['documents'][0] else ""
        
        # Generate answer with selected model
        answer = generate_answer(context, question, chat_history, selected_model)
        
        # Prepare response
        response_data = {
            'answer': answer,
            'timestamp': datetime.now().isoformat(),
            'context_used': bool(context),
            'context_length': len(context),
            'model_used': selected_model,
            'model_name': AVAILABLE_MODELS.get(selected_model, selected_model)
        }
        
        return jsonify(response_data)
        
    except Exception as e:
        return jsonify({'error': f'Sunucu hatası: {str(e)}'}), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001) 