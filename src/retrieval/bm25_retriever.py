import sys
from pathlib import Path

src_path = Path(__file__).resolve().parent.parent
if str(src_path) not in sys.path:
    sys.path.append(str(src_path))
    
import json
from rank_bm25 import BM25Okapi

with open("./data/contextualized_chunks.json", "r", encoding="utf-8") as file:
    chunks = json.load(file)

tokenized_chunks=[chunk["text"].lower().split() for chunk in chunks]

bm25=BM25Okapi(tokenized_chunks)

def bm25_retrieve(query,top_k=10):
    tokenized_query=query.lower().split()
    scores=bm25.get_scores(tokenized_query)
    top_indices=sorted(
        range(len(scores)),
        key=lambda i:scores[i],
        reverse=True
    )[:top_k]
    
    retrieved_chunks=[]
    
    for i in top_indices:
        chunk=chunks[i]
        retrieved_chunks.append({
            "id": f'{chunk["metadata"]["source"]}_{chunk["metadata"]["chunk_id"]}',
            "text": chunk["text"],
            "metadata": chunk["metadata"],
            "score": float(scores[i])
        })
        
    return retrieved_chunks
    
if __name__ == "__main__":
    results=bm25_retrieve(
        "RAG gives context to AI models",
        top_k=10
    )
    
    for result in results:
        print("\n--------------------")
        print("ID:", result["id"])
        print("Score:", result["score"])
        print("Text:", result["text"])
        print("Metadata:", result["metadata"])