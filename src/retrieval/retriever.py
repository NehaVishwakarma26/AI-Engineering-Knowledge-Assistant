import sys
from pathlib import Path

src_path = Path(__file__).resolve().parent.parent
if str(src_path) not in sys.path:
    sys.path.append(str(src_path))
    
from embeddings import embedder

import chromadb

def retrieve(query,top_k=3):
    client=chromadb.PersistentClient(path="./my_chroma_db")
    collection=client.get_collection(name="document_chunks")
    query_embedding=embedder.get_embeddings(query)
    
    results=collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    
    retrieved_chunks=[]
    for i,document in enumerate(results["documents"][0]):
        retrieved_chunks.append({
            "text":document,
            "metadata":results["metadatas"][0][i]
        })
    return retrieved_chunks

retrieved_chunks=retrieve("RAG is used to give more context to AI models")
print(f"\n\n Retrieved chunks are:")
print(f"\n{retrieved_chunks}")