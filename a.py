def embed_text(text):
    """
    Calling Groq Embedding API to turn the text into vectors.
    """
    try:
        response = client.embeddings.create(
            model="paraphrase-multilingual-MiniLM-L12-v2",  # Also tried with "paraphrase-multilingual-MiniLM-L12-v2" or "paraphrase-multilingual-mpnet-base-v2"
            input=text
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"[!] Embedding hatası: {e}")
        return [0.0]*1536  


def main():
    df = pd.read_csv('./data/chunked_data.csv')
    embeddings = []
    records = []
    with open('./data/embeddings.jsonl', 'w') as f:
        for idx, row in df.iterrows():
            embedding = embed_text(row['text'])
            embeddings.append(embedding)
            record = {
                'url': row['url'],
                'title': row['title'],
                'chunk': row['text'],
                'embedding': embedding
            }
            records.append(record)
            f.write(json.dumps(record) + '\n')
    print("✅ Embedding tamamlandı.")

    # Save embeddings as numpy array
    embedding_array = np.array(embeddings).astype("float32")
    np.save("./data/embeddings.npy", embedding_array)
    print("✅ Embedding array saved as embeddings.npy")


if __name__ == "__main__":
    main()
