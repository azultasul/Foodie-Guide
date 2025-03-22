from RAG import RAG

rag = RAG(RAG.HEALTH)
rag.load_vector_index()
print(rag.search_and_wrap("요로 결석이 있는 사람은 무엇을 조심해야돼?"))