import sys
from pathlib import Path

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

def get_embedding_batch(contextualized_chunks:list,model_name:str="embeddinggemma:latest")->list[list[float]]:
    
    texts=[
        chunk["contextualized_text"]
        for chunk in contextualized_chunks
    ]
    
    response=ollama.embed(
        model=model_name,
        input=texts
    )
    
    return response["embeddings"]

def store_chunks(contextualized_chunks,vectors):
    #    contextualized_chunks.append({
    #             "text":chunk,
    #             "context":generated_context,
    #             "contextualized_text":(
    #                 f"[Context: {generated_context}]\n\n"
    #                 f"[Original Chunk: {chunk}]"
    #             ),
    #             "metadata":{
    #                 "source":source,
    #                 "chunk_id":i
    #             }
    #         })
    
    client=chromadb.PersistentClient(path="./new_chroma_db")
    collection=client.get_or_create_collection(name="document_chunks")
    documents=[chunk["text"] for chunk in contextualized_chunks]
    metadata=[{
        "source":chunk["metadata"]["source"],
        "chunk_id":str(chunk["metadata"]["chunk_id"])
    } for chunk in contextualized_chunks
              ]
    ids=[
            f"{chunk["metadata"]["source"]}_{chunk["metadata"]["chunk_id"]}"
            for chunk in contextualized_chunks
        ]
    collection.upsert(documents=documents,embeddings=vectors,metadatas=metadata,ids=ids)
    print(f"Stored {len(documents)} chunks in Chroma")