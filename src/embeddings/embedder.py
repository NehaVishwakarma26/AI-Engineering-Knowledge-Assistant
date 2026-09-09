import sys
from pathlib import Path

# __file__ is chunker.py -> .parent is chunking/ -> .parent.parent is src/
src_path = Path(__file__).resolve().parent.parent
if str(src_path) not in sys.path:
    sys.path.append(str(src_path))

from chunking import chunker
import ollama
import chromadb

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

def store_chunks(chunks,vectors):
    client=chromadb.PersistentClient(path="./my_chroma_db")
    collection=client.get_or_create_collection(name="document_chunks")
    documents=[chunk['text'] for chunk in chunks]
    metadatas=[
        {
            "source":chunk["metadata"]["source"],
            "chunk_id":str(chunk["metadata"]["chunk_id"])
        }
        for chunk in chunks
    ]
    ids=[
        f"{chunk["metadata"]["source"]}_{chunk["metadata"]["chunk_id"]}"
        for chunk in chunks
    ]
    collection.add(
        documents=documents,
        embeddings=vectors,
        metadatas=metadatas,
        ids=ids
    )
    
if __name__=="__main__":
    chunks=chunker.chunk_docs()
    chunks_string=[chunk["text"] for chunk in chunks]
    vectors=get_embeddings_batch(chunks_string)
    store_chunks(chunks,vectors)
    print(f"stored {len(chunks)} chunks in chroadb")