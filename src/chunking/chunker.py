import sys
from pathlib import Path

# __file__ is chunker.py -> .parent is chunking/ -> .parent.parent is src/
src_path = Path(__file__).resolve().parent.parent
if str(src_path) not in sys.path:
    sys.path.append(str(src_path))

from ingestion import loader

def chunk_documents(documents,chunk_size,overlap):
    chunks=[]
    for doc in documents:
        text=doc["text"]
        source_file=doc["source"]
        
        start=0
        chunk_idx=0
        
        while(start<len(text)):
            end=start+chunk_size
            chunk=text[start:end]
            chunks.append({
                "text":chunk,
                "metadata":{
                    "source":source_file,
                    "chunk_id":chunk_idx
                }
            })
            
            chunk_idx+=1
            start+=chunk_size-overlap
    return chunks


def chunk_docs():
    documents=loader.load_files()
    processed_chunks=chunk_documents(documents,100,10)
    # for chunk in processed_chunks[:3]:
    #     print(f"source:{chunk['metadata']['source']} | ID: {chunk['metadata']['chunk_id']}")
    #     print(f"content:{chunk['text']}\n{'-'*30}")
    return processed_chunks
    