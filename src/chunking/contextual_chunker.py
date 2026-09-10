import sys
from pathlib import Path

src_path = Path(__file__).resolve().parent.parent
if str(src_path) not in sys.path:
    sys.path.append(str(src_path))

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

from ingestion import loader

# define llm
llm=ChatOllama(
    model="llama3.1:latest",
    temperature=0
)

# split text by 800 characters and a overlap of 100 characters
def rec_split(document_text):
    splitter=RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=100,
    separators=["\n\n","\n"," ",""]
    )
    chunks=splitter.split_text(document_text)
    return chunks


def generate_context(document_text,chunks,source):
    prompt=ChatPromptTemplate.from_template("""
    Here is the full document:
    <document>
    {document}
    </document>
    
    Here is the chunk we want to situate within the whole document:
    <chunk>
    {chunk}
    </chunk>
    
    
Please give a short, succinct context to situate this chunk
within the overall document.

Only use information that can be inferred from the document.
                                            """)
    
    chain = prompt|llm
    contextualized_chunks=[]
    
    for i,chunk in enumerate(chunks):
        print(f"Processing chunk {i+1}/{len(chunks)}....")
        
        response=chain.invoke({
            "document":document_text,
            "chunk":chunk
        })
        
        generated_context=response.content 
        
        contextualized_chunks.append({
            "text":chunk,
            "context":generated_context,
            "contextualized_text":(
                f"[Context: {generated_context}]\n\n"
                f"[Original Chunk: {chunk}]"
            ),
            "metadata":{
                "source":source,
                "chunk_id":i
            }
        })
        
    return contextualized_chunks    
    
def get_final_chunks():
    final_chunks=[]
    documents=loader.load_files()
    for doc in documents:
        document_text=doc["text"]
        base_chunks=rec_split(document_text)
        print(f"Created {len(base_chunks)} base chunks \n\n")
        chunks=generate_context(
            document_text,
            base_chunks,
            doc["source"]
        )
        print("\n\n Example:")
        print(chunks[0])
        final_chunks.extend(chunks)
    return final_chunks

final_chunks=get_final_chunks()
print(f"{len(final_chunks)} generated")
print(final_chunks[0])