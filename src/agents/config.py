import sys
from pathlib import Path

MODEL_NAME="qwen3:8b"

EXCLUDED_DIRS= {
    ".venv",
    ".git",
    "__pycache__",
    "new_chroma_db",
    "my_chroma_db",
}

_SRC_PATH = Path(__file__).resolve().parent.parent.parent
if str(_SRC_PATH) not in sys.path:
    sys.path.append(str(_SRC_PATH))
 