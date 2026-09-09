import sys
from pathlib import Path

src_path = Path(__file__).resolve().parent.parent
if str(src_path) not in sys.path:
    sys.path.append(str(src_path))

import ollama
from retrieval import retriever

def generate_answer(query,retrieved_chunks):
    text=""
    for chunk in retrieved_chunks:
        text+=chunk["text"]
        text+="\n\n"
        
    system_prompt="""
    You are a helpful assistant. Answer the user's question using only the provided context.
    If you do not know the answer based on the context, say "I cannot find the answer"
    """
        
    user_prompt=f"""
    You are a knowledge assistant.
    Strictly using the context given below find the answer to the question.
    If relevant context not present just say that you don't know the answer. 
    Don't hallucinate.
    
    Context:
    {text}
    
    Question:
    {query}
    """
    response=ollama.generate(
        model="llama3.1:latest",
        system=system_prompt,
        prompt=user_prompt
    )
    
    return response["response"]

