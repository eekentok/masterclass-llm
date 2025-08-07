import pandas as pd
from transformers import AutoTokenizer

def chunk_sentences(df, chunk_size=500, model_name="unsloth/llama-3-8b-bnb-4bit"):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    records = []
    current_chunk = []
    current_tokens = 0
    chunk_id = 0
    prev_url = None
    prev_title = None

    for idx, row in df.iterrows():
        sentence = row['sentence']
        url = row['url']
        title = row['title']
        sentence_tokens = len(tokenizer.encode(sentence, add_special_tokens=False))

        # If new document, flush current chunk
        if prev_url is not None and url != prev_url:
            if current_chunk:
                records.append({
                    'url': prev_url,
                    'title': prev_title,
                    'chunk': " ".join(current_chunk),
                    'chunk_id': chunk_id
                })
                chunk_id = 0
                current_chunk = []
                current_tokens = 0

        if current_tokens + sentence_tokens > chunk_size:
            if current_chunk:
                records.append({
                    'url': url,
                    'title': title,
                    'chunk': " ".join(current_chunk),
                    'chunk_id': chunk_id
                })
                chunk_id += 1
            current_chunk = [sentence]
            current_tokens = sentence_tokens
        else:
            current_chunk.append(sentence)
            current_tokens += sentence_tokens

        prev_url = url
        prev_title = title

    # Add last chunk
    if current_chunk:
        records.append({
            'url': prev_url,
            'title': prev_title,
            'chunk': " ".join(current_chunk),
            'chunk_id': chunk_id
        })

    return pd.DataFrame(records)

def main():
    df = pd.read_csv('./data/sentence_split_traf_data.csv')
    chunked_df = chunk_sentences(df, chunk_size=500)
    chunked_df.to_csv('./data/new_chunked_traf_data.csv', index=False)
    print("✅ Chunking completed. Output: new_chunked_traf_data.csv")

if __name__ == "__main__":
    main()