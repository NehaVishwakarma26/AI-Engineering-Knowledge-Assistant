from src.chunking.contextual_chunker import get_final_chunks
from src.embeddings.contextual_embedder import get_embedding_batch,store_chunks

chunks=get_final_chunks()
vectors=get_embedding_batch(chunks)
store_chunks(chunks,vectors)