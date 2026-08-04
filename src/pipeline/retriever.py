import numpy as np
from typing import List, Dict, Any
from src.security.rbac import rbac_filter
from src.pipeline.embedding import embedding_generator


class VectorRetriever:
    """Enterprise Vector Store Retriever performing real Cosine Similarity search with RBAC filtering."""

    def __init__(self):
        # Initializing enterprise document knowledge base
        self.mock_db = [
            {
                "id": "doc-001",
                "content": "Enterprise Cloud Landing Zone Guidelines state that all production database instances must enable multi-region replication and automated 30-day snapshot backups.",
                "metadata": {"source": "cloud_policy.pdf", "allowed_roles": ["cloud_admin", "devops"]}
            },
            {
                "id": "doc-002",
                "content": "Context Engineering prompt length should not exceed 4096 tokens for standard latency tier requests. PII sanitization is strictly enforced.",
                "metadata": {"source": "genai_handbook.pdf", "allowed_roles": ["developer", "data_scientist"]}
            },
            {
                "id": "doc-003",
                "content": "Customer account data must be accessed only via authorized GraphQL endpoints requiring OAuth2 Bearer tokens with scope 'read:customer'.",
                "metadata": {"source": "security_standards.pdf", "allowed_roles": ["developer"]}
            }
        ]

        # Compute vector embeddings for knowledge base documents
        for doc in self.mock_db:
            doc["embedding"] = embedding_generator.generate_embedding(doc["content"])

    def cosine_similarity(self, vec_a: List[float], vec_b: List[float]) -> float:
        a = np.array(vec_a, dtype=np.float32)
        b = np.array(vec_b, dtype=np.float32)
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return float(np.dot(a, b) / (norm_a * norm_b))

    def retrieve(self, query: str, user_roles: List[str], top_k: int = 2) -> List[Dict[str, Any]]:
        # 1. Filter documents based on user RBAC permissions
        authorized_docs = rbac_filter.filter_documents(self.mock_db, user_roles)
        
        if not authorized_docs:
            return []

        # 2. Compute query embedding
        query_vec = embedding_generator.generate_embedding(query)

        # 3. Calculate cosine similarity for all authorized docs
        scored_docs = []
        for doc in authorized_docs:
            score = self.cosine_similarity(query_vec, doc["embedding"])
            scored_doc = doc.copy()
            scored_doc["similarity_score"] = round(score, 4)
            scored_docs.append(scored_doc)

        # 4. Sort descending by similarity score
        scored_docs.sort(key=lambda x: x["similarity_score"], reverse=True)
        return scored_docs[:top_k]


vector_retriever = VectorRetriever()
