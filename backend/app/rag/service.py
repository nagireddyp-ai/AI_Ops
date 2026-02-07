from dataclasses import dataclass
from typing import List

import chromadb
from chromadb.config import Settings
import ollama


@dataclass
class RAGResult:
    answer: str
    sources: List[str]


class RAGService:
    def __init__(self, collection_name: str = "sitepulse-kb") -> None:
        self.client = chromadb.Client(Settings(anonymized_telemetry=False))
        self.collection = self.client.get_or_create_collection(name=collection_name)

    def embed_documents(self, ids: List[str], documents: List[str], metadata: List[dict]) -> None:
        embeddings = ollama.embeddings(model="nomic-embed-text", prompt=documents)
        vectors = embeddings["embedding"] if isinstance(embeddings, dict) else embeddings
        self.collection.add(ids=ids, documents=documents, embeddings=vectors, metadatas=metadata)

    def query(self, question: str, k: int = 3) -> RAGResult:
        result = self.collection.query(query_texts=[question], n_results=k)
        sources = []
        if result.get("documents"):
            for doc in result["documents"][0]:
                sources.append(doc[:80])
        response = ollama.generate(model="llama3.1:8b", prompt=question)
        answer = response["response"] if isinstance(response, dict) else str(response)
        return RAGResult(answer=answer, sources=sources)
