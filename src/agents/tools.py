from pathlib import Path
from config import EXCLUDED_DIRS
from api_generator import search_knowledge_api

tool_schemas={
    "search_knowledge":{
        "required":["query"]
    },
    "list_files":{
        "required":[]
    },
    "read_file":{
        "required":["path"]
    }
}

def search_knowledge(query:str)->str:
    """Search the engineering knowledge base for conceptual and technical information.

    Use this for general explanations, concepts, algorithms, architecture,
    documentation, and engineering knowledge.

    This tool searches the knowledge base, NOT the actual project source code."""
    
    """
    Args:
    query: The question to be asked
    
    Returns:
    The answer to the query from the knowledge base
    """
    return search_knowledge_api(query)

def read_file(path:str):
    """Read the contents of an actual file in the current project.

    Use this only when you know the exact project-relative file path.
    If you do not know the exact path, use list_files first to discover it.

    Args:
        path: Relative path of the file inside the project.

    Returns:
        The file's contents, or a description of what went wrong.
    """
    
    directory=Path.cwd().resolve()
    requested_path=Path(path)
    
    if requested_path.is_absolute():
        return {"Error": "path must be relative to the project directory.",
                "path":path}
    
    file_path=(directory/requested_path).resolve()
    
    if directory not in file_path.parents:
        return {"error": "file is outside the project directory",
                "path":path,}
    
    if not file_path.exists():
        matches=[
            str(file.relative_to(directory))
            for file in directory.rglob(requested_path.name)
            if file.is_file()
            and not any(part in EXCLUDED_DIRS for part in file.parts)
        ]
        
        return {
            "error":"File not found.",
            "path":path,
            "possible_matches":matches[:5],
            "hint":"Use list_files to discover the exact project-relative path."
        }
        
    if not file_path.is_file():
        return {
            "error":"Path is not a file",
            "path":path
        }
        
    try:
        return file_path.read_text(encoding="utf-8")
    
    except UnicodeDecodeError:
        return {
            "error":"Unable to decode file as UTF-8",
            "path":path
        }
        
def list_files():
    """List all the files in the project"""
    
    directory=Path.cwd()
    
    files=[str(f.relative_to(directory)) for f in directory.rglob("*") if f.is_file()
           and not any(part in EXCLUDED_DIRS for part in f.parts)]
    return files    

available_functions={
    'search_knowledge':search_knowledge,
    'list_files':list_files,
    'read_file':read_file
}

TOOLS=[search_knowledge,list_files,read_file]