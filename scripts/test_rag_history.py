#!/usr/bin/env python3

"""
test_rag_history.py

RAG-based chat history sistemini test etmek için (RAM-based)
"""

from rag import store_conversation_turn, retrieve_relevant_history, format_chat_history_for_prompt, chat_history
import uuid

def test_ram_rag_history():
    """
    RAM-based RAG chat history sistemini test et
    """
    print("🧪 RAM-based RAG Chat History Test")
    print("=" * 50)
    
    # Test session ID'si oluştur
    session_id = str(uuid.uuid4())
    print(f"Session ID: {session_id}")
    
    # Örnek konuşmaları kaydet
    test_conversations = [
        ("Vadeli mevduat nedir?", "Vadeli mevduat, belirli bir süre için bankaya yatırılan paradır."),
        ("Faiz oranları nasıl belirlenir?", "Faiz oranları Merkez Bankası tarafından belirlenir."),
        ("Kredi kartı limiti nasıl artırılır?", "Kredi kartı limiti düzenli ödemelerle artırılabilir."),
        ("Banka hesabı nasıl açılır?", "Banka hesabı kimlik belgesi ile açılabilir."),
        ("Yatırım fonları güvenli mi?", "Yatırım fonları çeşitli risk seviyelerinde bulunur.")
    ]
    
    print("\n📝 Test konuşmaları RAM'e kaydediliyor...")
    for question, answer in test_conversations:
        store_conversation_turn(question, answer, session_id)
        print(f"✓ {question[:30]}...")
    
    # Test sorguları
    test_queries = [
        "Vadeli mevduat hakkında bilgi verir misin?",
        "Faiz konusunda ne biliyorsun?",
        "Kredi kartı ile ilgili bilgi var mı?",
        "Banka hesabı açmak istiyorum",
        "Yatırım yapmak istiyorum"
    ]
    
    print("\n🔍 İlgili geçmiş konuşmalar aranıyor...")
    for query in test_queries:
        print(f"\nSoru: {query}")
        relevant_conversations, metadatas = retrieve_relevant_history(query, session_id, top_k=3)
        
        if relevant_conversations:
            print("İlgili konuşmalar:")
            for i, conv in enumerate(relevant_conversations[:2]):  # İlk 2'sini göster
                print(f"  {i+1}. {conv[:100]}...")
        else:
            print("  İlgili konuşma bulunamadı.")
    
    # Session bilgilerini göster
    print(f"\n📊 Session İstatistikleri:")
    print(f"Toplam konuşma sayısı: {len(chat_history.conversations)}")
    print(f"Session sayısı: {len(chat_history.session_embeddings)}")
    print(f"Bu session'daki konuşma sayısı: {len(chat_history.session_embeddings.get(session_id, []))}")
    
    # Session konuşmalarını listele
    session_conversations = chat_history.get_session_conversations(session_id)
    print(f"\n📋 Bu session'daki tüm konuşmalar:")
    for i, conv in enumerate(session_conversations):
        print(f"  {i+1}. {conv['metadata']['question'][:50]}...")
    
    print("\n✅ RAM-based test tamamlandı!")

def test_performance():
    """
    RAM-based sistemin performansını test et
    """
    print("\n⚡ Performans Testi")
    print("=" * 30)
    
    import time
    
    # Çok sayıda konuşma ekle
    start_time = time.time()
    
    for i in range(100):
        question = f"Test sorusu {i} nedir?"
        answer = f"Test cevabı {i} budur."
        store_conversation_turn(question, answer, "perf_test_session")
    
    storage_time = time.time() - start_time
    print(f"100 konuşma ekleme süresi: {storage_time:.3f} saniye")
    
    # Arama performansını test et
    start_time = time.time()
    for i in range(10):
        query = f"Test sorgusu {i}"
        retrieve_relevant_history(query, "perf_test_session", top_k=5)
    
    search_time = time.time() - start_time
    print(f"10 arama süresi: {search_time:.3f} saniye")
    
    print(f"Toplam konuşma sayısı: {len(chat_history.conversations)}")
    print("✅ Performans testi tamamlandı!")

if __name__ == "__main__":
    test_ram_rag_history()
    test_performance() 