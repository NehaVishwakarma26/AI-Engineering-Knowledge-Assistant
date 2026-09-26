import sys
from pathlib import Path

src_path = Path(__file__).resolve().parent.parent
if str(src_path) not in sys.path:
    sys.path.append(str(src_path))
    
from retrieval.retriever import retrieve
from retrieval.bm25_retriever import bm25_retrieve
from retrieval.reranker import rerank

def reciprocal_rank_fusion(dense_results,bm25_results,k=60,top_k=3):
    rrf_scores={}
    result_lookup={}
    
    for rank,result in enumerate(dense_results,start=1):
        chunk_id=result["id"]
        
        result_lookup[chunk_id]=result
        
        rrf_scores[chunk_id]=(
            rrf_scores.get(chunk_id,0)
            + 1/(k+rank)
        )
        
    for rank,result in enumerate(bm25_results,start=1):
        chunk_id=result["id"]
        result_lookup[chunk_id]=result
        rrf_scores[chunk_id]=(
            rrf_scores.get(chunk_id,0)
            + 1/(k+rank)
        )
    
    # print("k=",k)
    # print("RRF scores =",rrf_scores)
        
    ranked_chunks=sorted(
        rrf_scores.items(),
        key=lambda item:item[1],
        reverse=True
    )
    
    final_results=[]
    
    for chunk_id,score in ranked_chunks[:top_k]:
        result=result_lookup[chunk_id].copy()
        result["rrf_score"]=score
        final_results.append(result)
    
    return final_results

if __name__ == "__main__":

    query = "RAG gives context to AI models"

    dense_results = retrieve(query, top_k=10)

    bm25_results = bm25_retrieve(query, top_k=10)

    hybrid_results = reciprocal_rank_fusion(
        dense_results,
        bm25_results,
        k=60,
        top_k=10
    )
    
    reranked_results=rerank(query,hybrid_results,top_k=3)

    # print("\n\nRERANKED RESULTS")

    # for result in reranked_results:

    #     print("\n--------------------")
    #     print("ID:", result["id"])
    #     print("RRF Score:", result["rrf_score"])
    #     print("Text:", result["text"])
    #     print("Metadata:", result["metadata"])
    #     print("Similarity Score", result["sim_score"])