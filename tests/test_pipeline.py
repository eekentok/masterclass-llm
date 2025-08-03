# tests/test_pipeline.py

"""
test_pipeline.py

Amaç:
- Basit test kontrolleri
"""

import pandas as pd

def test_no_empty_rows():
    """
    Cleaned CSV'de boş satır var mı kontrol et.
    """
    df = pd.read_csv('output/cleaned_data.csv')
    assert not df.isnull().any().any(), "❌ Cleaned CSV içinde boş satır(lar) var!"

def test_chunk_length(max_length=500):
    """
    Chunk uzunluğu limit kontrolü (kelime bazlı).
    """
    df = pd.read_csv('output/chunked_data.csv')
    for i, row in df.iterrows():
        words = str(row['chunk']).split()
        assert len(words) <= max_length, f"❌ Chunk {i} kelime sınırını aşıyor: {len(words)} kelime"
    
