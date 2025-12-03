import os

import sentence_transformers

os.listdir

def embed(chunk):
    return sentence_transformers.SentenceTransformer('all-MiniLM-L6-v2').encode(chunk).tolist()

def chunk_and_embed(document):
    embeddings = []
    for chunk in document.splitlines():
        if chunk != "":
            embeddings.append(embed(chunk))

        return embeddings

def main():
    dirpath = "rag_docs/"
    files = os.listdir(dirpath)
    all_chunked_embeddings = []
    for file in files:
        with open(dirpath + file, 'r') as f:
            document = f.read()
            all_chunked_embeddings.append(chunk_and_embed(document))
        

if __name__ == "__main__":
    main()
