import sys
from pathlib import Path
import json

src_path = Path(__file__).resolve().parent.parent.parent
if str(src_path) not in sys.path:
    sys.path.append(str(src_path))

from api_generator import search_knowledge_api

from ollama import chat,ChatResponse
print("Asking question...")

tool_schemas={
    "search_knowledge":{
        "required":["query"]
    }
}

def search_knowledge(query:str)->str:
    """Search knowledge base and return relevant evidence"""
    
    """
    Args:
    query: The question to be asked
    
    Returns:
    The answer to the query from the knowledge base
    """
    return search_knowledge_api(query)

available_functions={
    'search_knowledge':search_knowledge
}

messages=[
    {
        "role":"user",
        "content":"What is RAG?"
    }
]

while True:
    response: ChatResponse=chat(
        model="llama3.1:latest",
        messages=messages,
        tools=[search_knowledge],
        think=False,
    )
    
    messages.append(response.message)
    print("Thinking: ",response.message.thinking)
    print("Content: ",response.message.content)
    if response.message.tool_calls:
        for tc in response.message.tool_calls:
            if tc.function.name in available_functions:
                print(f"Calling {tc.function.name} with arguments {tc.function.arguments}")
                required_arguments=tool_schemas[tc.function.name]["required"]
                
                missing_arguments=[
                    arg for arg in required_arguments
                    if arg not in tc.function.arguments
                ]
                
                if missing_arguments:
                    error={
                        "error":"Missing required arguments",
                        "missing":missing_arguments
                    }
                    messages.append({
                        "role":"tool",
                        "tool_name":tc.function.name,
                        "content":json.dumps(error)
                    })
                    continue
                
                result=available_functions[tc.function.name](**tc.function.arguments)
                print(f"Result: {result}")
                
                messages.append({
                    "role":"tool",
                    "tool_name":tc.function.name,
                    "content":json.dumps(result)
                })
        
    else:
        print("Final answer:",response.message.content)
        break
                
