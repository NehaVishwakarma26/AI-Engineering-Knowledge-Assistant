from sentence_transformers import CrossEncoder

MODEL_NAME="cross-encoder/ms-marco-MiniLM-L-6-v2"
reranker=CrossEncoder(MODEL_NAME)

def rerank(query,retrieved_chunks,top_k=3):
    sentence_pairs=[[query,chunk["text"]] for chunk in retrieved_chunks]
    similarity_scores=reranker.predict(sentence_pairs)
    for idx in range(len(retrieved_chunks)):
        retrieved_chunks[idx]["sim_score"]=float(similarity_scores[idx])
        
    retrieved_chunks.sort(key=lambda x:x['sim_score'],reverse=True)
    
    return retrieved_chunks[:top_k]
    
  
if __name__ == "__main__":
    chunks = [
        {"text": "RAG combines retrieval with language model generation."},
        {"text": "Docker packages applications into containers."},
        {"text": "BM25 is a lexical retrieval algorithm."}
    ]

    results = rerank(
        "What is RAG?",
        chunks,
        top_k=2
    )

    # for result in results:
    #     print(result)