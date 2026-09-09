from pathlib import Path

def load_files():
    content=[]
    folder_path=Path("./data/documents")
    
    for file_path in folder_path.glob("*.txt"):
        with open(file_path,"r",encoding="utf-8") as file:
            d={"text":file.read(),"source":file_path.name}
            content.append(d)
    return content
            
documents=load_files()
print(documents)