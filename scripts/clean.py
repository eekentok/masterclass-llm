# scripts/clean.py

#!/usr/bin/env python3

"""
clean.py

Amaç:
- HTML ve gereksiz karakterleri temizle
- Lower-case
"""

import pandas as pd
import re

def clean_text(text):
    if not text or not isinstance(text, str):
        return ""
        
    # Clean HTML tags.
    text = re.sub(r'<[^>]+>', ' ', text)
    # Lowercase.
    text = text.lower()
    # Delete punctuation.
    text = re.sub(r"[^\w\s]", " ", text)
    # Delete unnecessary spaces.
    text = re.sub(r"\s+", " ", text).strip()
    return text


def main():
    df = pd.read_csv("../input/scraped_data.csv")

    # Clean content column.
    df["clean_content"] = df["content"].apply(clean_text)

    df.to_csv("../output/cleaned_data.csv", index=False)
    print("✅ Temizlik tamamlandı. → output/cleaned_data.csv")

if __name__ == "__main__":
    main()
