# scripts/run_pipeline.sh

#!/bin/bash
echo "📌 Pipeline başlatılıyor..."
echo "Başlamak istediğiniz adımı seçin:"
# TODO: Adımları sırayla çalıştır
echo "1. Veritabanı temizleme"
echo "2. Veritabanı oluşturma"
echo "3. RAG modeli oluşturma"
echo "-m: LLM Modellerini yönetme"
echo "-c: RAG modeli ile soru cevaplama"
read -p "Seçiminiz : " step
case $step in
    1)
        echo "Veritabanı temizleniyor..."
        python scripts/clean.py
        echo "Veritabanı temizleme tamamlandı."
        echo ""
        ;;
    2)
        echo "Veritabanı oluşturuluyor..."
        python scripts/create_db.py
        ;;
    3)
        echo "RAG modeli oluşturuluyor..."
        python scripts/rag.py --create_model
        ;;
    -m)
        echo "LLM modelleri yönetiliyor..."
        python scripts/manage_models.py
        ;;
    -c)
        echo "RAG modeli ile soru cevaplama başlatılıyor..."
        python scripts/rag.py --ask_question
        ;;
    *)
        echo "Geçersiz seçim. Lütfen 1-4 arasında bir sayı girin."
        exit 1
        ;;
esac

echo "✅ Pipeline tamamlandı."
