from typing import List, Dict, Any


class RBACFilter:
    """Enforces Document Security Clearances against user roles."""

    def filter_documents(self, documents: List[Dict[str, Any]], user_roles: List[str]) -> List[Dict[str, Any]]:
        if "admin" in user_roles or "global_read" in user_roles:
            return documents

        authorized_docs = []
        for doc in documents:
            required_roles = doc.get("metadata", {}).get("allowed_roles", [])
            # If no roles specified, doc is public inside the enterprise
            if not required_roles:
                authorized_docs.append(doc)
            elif any(role in user_roles for role in required_roles):
                authorized_docs.append(doc)

        return authorized_docs


rbac_filter = RBACFilter()
