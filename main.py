
from src.retrieval.retriever import retrieve
from src.generation.generator import generate_answer

query="What is RAG?"

chunks=retrieve(query,top_k=3)
answer=generate_answer(query,chunks)

print("\nAnswer")
def main():
    print("Hello from assistant!")


if __name__ == "__main__":
    main()
