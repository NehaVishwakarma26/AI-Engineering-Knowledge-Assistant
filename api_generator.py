from src.retrieval.retriever import retrieve
from src.retrieval.bm25_retriever import bm25_retrieve
from src.retrieval.hybrid_retriever import reciprocal_rank_fusion
from src.retrieval.reranker import rerank
from src.generation.generator import generate_answer
def generate_answer_api(query:str):
    dense_results=retrieve(query,top_k=10)
    bm25_results=bm25_retrieve(query,top_k=10)
    
    hybrid_results=reciprocal_rank_fusion(
        dense_results,
        bm25_results,
        k=60,
        top_k=10
    )
    
    reranked_results=rerank(
        query,
        hybrid_results,
        top_k=3
    )
    
    print("\n\n reranked results")
    
    for res in reranked_results:
        print(res)
    
    answer=generate_answer(query,reranked_results)
    
    return answer

def search_knowledge_api(query:str):
    dense_results=retrieve(query,top_k=10)
    bm25_results=bm25_retrieve(query,top_k=10)
    
    hybrid_results=reciprocal_rank_fusion(
        dense_results,
        bm25_results,
        k=60,
        top_k=10
    )
    
    reranked_results=rerank(
        query,
        hybrid_results,
        top_k=3
    )
    
    return reranked_results