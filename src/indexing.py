import json

from embeddings.contextual_embedder import get_embedding_batch, store_chunks


CACHE_PATH = "./data/contextualized_chunks.json"


def index_documents():
    with open(CACHE_PATH, "r", encoding="utf-8") as file:
        chunks = json.load(file)

    print(f"Loaded {len(chunks)} contextualized chunks")

    vectors = get_embedding_batch(chunks)

    print(f"Generated {len(vectors)} embeddings")

    store_chunks(chunks, vectors)

    print("Indexing complete")


if __name__ == "__main__":
    index_documents()