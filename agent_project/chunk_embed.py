import os

import sentence_transformers
import numpy as np

os.listdir

model = sentence_transformers.SentenceTransformer('all-MiniLM-L6-v2')

def embed(chunk):
    return model.encode(chunk).tolist()

def chunk_and_embed(document):
    embeddings = []
    chunks = []
    for chunk in document.split("\n"):
        if chunk != "":
            embeddings.append(embed(chunk))
            chunks.append(chunk)

    return embeddings, chunks

def main():
    dirpath = "rag_docs/"
    files = os.listdir(dirpath)
    all_chunked_embeddings = []
    all_chunks = []
    for file in files:
        if not file.endswith(".txt"):
            continue
        print(f"Embedding document {file}")
        with open(dirpath + file, 'r', encoding='utf-8', errors='ignore') as f:
            document = f.read()
            embeddings, chunks = chunk_and_embed(document)
            all_chunked_embeddings.extend(embeddings)
            all_chunks.extend(chunks)

    np.save("embeddings.npy", np.array(all_chunked_embeddings, dtype=np.float32))
    with open("chunks.npy", 'wb') as f:
        np.save(f, np.array(all_chunks, dtype=object))
        

if __name__ == "__main__":
    main()
