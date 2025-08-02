# scripts/run_pipeline.sh

echo "📌 Pipeline başlatılıyor..."

echo "📥 1. Scraping başlatılıyor..."
python3 scripts/scrapper.py

echo "🧼 2. Temizleme işlemi başlatılıyor..."
python3 scripts/clean.py

echo "🔪 3. Chunking işlemi başlatılıyor..."
python3 scripts/chunk.py

echo "🧠 4. Embedding başlatılıyor..."
python3 scripts/embed.py

echo "✅ Pipeline tamamlandı."
