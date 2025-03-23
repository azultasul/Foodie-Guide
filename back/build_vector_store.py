from RAG import RAG

rag = RAG(RAG.HEALTH)
rag.save_vector_index()

rag = RAG(RAG.INGREDIENTS)
rag.save_vector_index()