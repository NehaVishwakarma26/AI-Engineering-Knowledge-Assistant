import sys
from pathlib import Path

# __file__ is chunker.py -> .parent is chunking/ -> .parent.parent is src/
src_path = Path(__file__).resolve().parent.parent
if str(src_path) not in sys.path:
    sys.path.append(str(src_path))

from chunking import chunker

import ollama

def get_embeddings(text:str,model_name:str="embeddinggemma:latest")->list[float]:
    """Generate a raw embedding vector using a locally running Ollama instance"""
    
    response = ollama.embed(
        model=model_name,
        input=text
    )
    
    return response['embeddings'][0]

def get_embeddings_batch(text:list[str],model_name:str="embeddinggemma:latest")->list[float]:
    
    response=ollama.embed(
        model=model_name,
        input=text
    )
    
    return response['embeddings']

if __name__=="__main__":
    sample_text="Retrieval Augmented Generation handles complex local documents."
    vector=get_embeddings(sample_text)
    
    print("Vector calculation successful")
    print(f"Embedding dimensions: {len(vector)}") 
    print(f"snippet sample: {vector[:5]}...\n")
    
    chunks=chunker.chunk_docs()
    chunks_string=chunks_string = [
    f"{chunk['metadata']['source']} {str(chunk['metadata']['chunk_id'])} {chunk['text']}" 
    for chunk in chunks
]
    vectors=get_embeddings_batch(chunks_string)
    print("\n\n\n")
    print("embedding batches")
    for i,vec in enumerate(vectors[:3]):
        print(f"vector {i+1} preview first 5 dimensions {vec[:5]}")