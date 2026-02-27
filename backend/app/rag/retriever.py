import chromadb
from chromadb.utils import embedding_functions
from backend.app.core.config import settings
from typing import List, Dict

class RAGRetriever:
    def __init__(self):
        self.chroma_client = chromadb.PersistentClient(path=settings.CHROMA_PATH)
        if settings.OPENAI_API_KEY:
            self.embedding_function = embedding_functions.OpenAIEmbeddingFunction(
                api_key=settings.OPENAI_API_KEY,
                model_name="text-embedding-3-small"
            )
        else:
            # Fallback to local default embeddings (all-MiniLM-L6-v2) for Groq-only setups
            self.embedding_function = embedding_functions.DefaultEmbeddingFunction()
        self.collection = self.chroma_client.get_or_create_collection(
            name="resumes",
            embedding_function=self.embedding_function
        )

    def add_resume(self, resume_id: str, text: str, metadata: dict):
        self.collection.upsert(
            documents=[text],
            metadatas=[metadata],
            ids=[resume_id]
        )

    def query_matching_resumes(self, job_description: str, n_results: int = 3) -> List[Dict]:
        results = self.collection.query(
            query_texts=[job_description],
            n_results=n_results
        )
        return results

    def get_resume(self, resume_id: str) -> str:
        """Retrieves the full text of a specific resume by its ID (filename)."""
        res = self.collection.get(ids=[resume_id])
        if res and res["documents"]:
            # Returns the first document associated with this ID
            return res["documents"][0]
        return ""

rag_retriever = RAGRetriever()
