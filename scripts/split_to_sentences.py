import pandas as pd
from langdetect import detect
import stanza
import spacy_stanza

# Pipelineleri yükle
nlp_tr = spacy_stanza.load_pipeline("tr")
nlp_en = spacy_stanza.load_pipeline("en")

def split_sentences(text):
    lang = detect(text)
    if lang == "tr":
        doc = nlp_tr(text)
    elif lang == "en":
        doc = nlp_en(text)
    else:
        doc = nlp_tr(text)
    return [sent.text.strip() for sent in doc.sents]

def main():
    df = pd.read_csv('./data/cleaned_traf_data.csv')
    records = []
    for idx, row in df.iterrows():
        content = row['content']
        title = row.get('title', f'Row {idx}')
        url = row['url']
        sentences = split_sentences(content)
        for sent_id, sentence in enumerate(sentences):
            records.append({
                'url': url,
                'title': title,
                'sentence': sentence,
                'sentence_id': sent_id
            })
    out_df = pd.DataFrame(records)
    out_df.to_csv('./data/sentence_split_traf_data.csv', index=False)
    print("✅ Sentence splitting completed. Output: sentence_split_traf_data.csv")

if __name__ == "__main__":
    main()