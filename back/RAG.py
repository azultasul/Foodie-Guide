import pickle
from langchain_text_splitters import RecursiveCharacterTextSplitter
import numpy as np
import openai
import faiss
import os
from tqdm import tqdm

import dotenv
dotenv.load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

class RAG(object):

    HEALTH = "health"
    INGREDIENTS = "ingredients"

    def __init__(self, filename = HEALTH):
        self.filename = filename
        self.index = None
        self.chunks = None

    def get_embedding(self, texts):
        response = openai.embeddings.create(
            model="text-embedding-3-small",
            input=texts
        )
        
        return [item.embedding for item in response.data]
    
    def get_embedding_one(self, text):
        return self.get_embedding(text)[0]
    
    def batched_embeddings(self, chunks, epoch_size=1000): # For 문으로 batch 없이 처리하면 너무 많이 요청해서 batch 함수 만듬 
        """
        chunks: List[str] - 임베딩할 텍스트 조각들
        epoch_size: int - 한 번에 처리할 최대 텍스트 수 (배치 크기)
        """
        all_embeddings = []

        # 총 epoch 수 계산
        total = len(chunks)
        for i in tqdm(range(0, total, epoch_size), desc="Embedding batches"):
            batch = chunks[i:i+epoch_size]
            
            # get_embedding은 한 번에 여러 개의 텍스트를 처리하는 함수라고 가정
            batch_embeddings = self.get_embedding(batch)
            
            # 결과 합치기
            all_embeddings.extend(batch_embeddings)
        
        return all_embeddings

    def save_vector_index(self):
        with open(f"docs/{self.filename}.txt", "r", encoding="utf-8") as f:
            raw_text = f.read()
        print("✅1/5 파일 호출 완료!")

        # 2. 텍스트 청크로 나누기
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = splitter.split_text(raw_text)
        print("✅2/5 청크 생성 완료!")

        # 3. 청크 임베딩
        N = len(chunks)
        print("청크 개수:", N)
        embeddings = self.batched_embeddings(chunks)
        embeddings_np = np.array(embeddings).astype("float32")
        print("✅3/5 청크 임베딩 완료!")

        # 4. FAISS 인덱스 생성 및 저장
        dimension = len(embeddings[0])
        index = faiss.IndexFlatL2(dimension)
        index.add(embeddings_np)

        faiss.write_index(index, f"vector_store/index_{self.filename}.faiss")
        print("✅4/5 FAISS 인덱스 저장 완료!")

        # 👉 청크도 함께 저장
        with open(f"vector_store/chunks_{self.filename}.pkl", "wb") as f:
            pickle.dump(chunks, f)

        print("✅5/5 임베딩 저장 완료!")

    def load_vector_index(self):
        self.index = faiss.read_index(f"vector_store/index_{self.filename}.faiss")

        with open(f"vector_store/chunks_{self.filename}.pkl", "rb") as f:
            self.chunks = pickle.load(f)
    
    def search_and_wrap(self, question):
        query_embedding = np.array([self.get_embedding_one(question)]).astype("float32")
        if self.index is not None:
            D, I = self.index.search(query_embedding, k=5)
            retrieved_chunks =  [self.chunks[i] for i in I[0]]
            print("[추가된 RAG 청크]", retrieved_chunks)
            prompt = "다음 정보를 바탕으로 질문에 답해줘:\n\n"
            prompt += "\n\n".join(retrieved_chunks)
            prompt += f"\n\n질문: {question}"
        else:
            prompt = question
        return prompt