#!/bin/bash

# İş Bankası AI Chatbot Web Interface Startup Script

echo "🚀 İş Bankası AI Chatbot Web Interface başlatılıyor..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Virtual environment oluşturuluyor..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Virtual environment aktifleştiriliyor..."
source venv/bin/activate

# Install/update requirements
echo "📚 Gereksinimler yükleniyor..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env dosyası bulunamadı!"
    echo "📝 Lütfen .env dosyası oluşturun ve API_KEY değişkenini ayarlayın:"
    echo "API_KEY=your_groq_api_key_here"
    exit 1
fi

# Check if data directory and ChromaDB exist
if [ ! -d "data/chroma_db" ]; then
    echo "⚠️  ChromaDB veritabanı bulunamadı!"
    echo "📝 Lütfen önce veri pipeline'ını çalıştırın:"
    echo "bash scripts/run_pipeline.sh"
    exit 1
fi

# Start the web interface
echo "🌐 Web interface başlatılıyor..."
echo "📍 Tarayıcınızda http://localhost:5000 adresini açın"
echo "🛑 Durdurmak için Ctrl+C tuşlarına basın"
echo ""

python app.py 