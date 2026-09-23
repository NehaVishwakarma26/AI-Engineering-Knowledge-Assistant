import sys
from pathlib import Path

src_path = Path(__file__).resolve().parent.parent
if str(src_path) not in sys.path:
    sys.path.append(str(src_path))
    
from embeddings import embedder

import chromadb

def retrieve(query,top_k=10):
    client=chromadb.PersistentClient(path="./new_chroma_db")
    collection=client.get_collection(name="document_chunks")
    query_embedding=embedder.get_embeddings(query)
    
    results=collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    
    retrieved_chunks=[]
    for i,document in enumerate(results["documents"][0]):
        metadata=results["metadatas"][0][i]
        retrieved_chunks.append({
            "id":f'{metadata["source"]}_{metadata["chunk_id"]}',
            "text":document,
            "metadata":metadata,
            "score":results["distances"][0][i]
        })
        
    
    return retrieved_chunks

if __name__ == "__main__":

    results = retrieve(
        "RAG gives context to AI models",
        top_k=10
    )

    for result in results:
        print("\n--------------------")
        print("ID:", result["id"])
        print("Score:", result["score"])
        print("Text:", result["text"])
        print("Metadata:", result["metadata"])