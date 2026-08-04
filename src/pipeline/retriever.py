from typing import List, Dict, Any
from src.security.rbac import rbac_filter


class VectorRetriever:
    def __init__(self):
        # Sample Enterprise Knowledge Base Documents
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

    def retrieve(self, query: str, user_roles: List[str], top_k: int = 2) -> List[Dict[str, Any]]:
        # Filter documents based on RBAC first
        authorized_docs = rbac_filter.filter_documents(self.mock_db, user_roles)
        # Return top_k documents
        return authorized_docs[:top_k]


vector_retriever = VectorRetriever()
