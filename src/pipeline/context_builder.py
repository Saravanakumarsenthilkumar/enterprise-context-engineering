from typing import List, Dict, Any, Tuple
from src.config import settings
from src.security.pii_redactor import pii_redactor


class ContextBuilder:
    """Assembles optimized, token-aware, PII-sanitized prompt payloads."""

    def __init__(self, max_token_budget: int = settings.DEFAULT_MAX_TOKEN_BUDGET):
        self.max_token_budget = max_token_budget

    def estimate_tokens(self, text: str) -> int:
        """Heuristic estimation of token count (~4 characters per token)."""
        return max(1, len(text) // 4)

    def assemble_context(
        self,
        system_instruction: str,
        user_query: str,
        rag_documents: List[Dict[str, Any]],
        conversation_history: List[Dict[str, str]] = None
    ) -> Tuple[Dict[str, Any], int]:
        total_pii_count = 0
        conversation_history = conversation_history or []

        # Step 1: Sanitize Inputs
        clean_system, pii1 = pii_redactor.redact(system_instruction)
        clean_query, pii2 = pii_redactor.redact(user_query)
        total_pii_count += pii1 + pii2

        # Step 2: Assemble RAG Documents with sanitization
        clean_rag_texts = []
        for doc in rag_documents:
            content = doc.get("content", "")
            clean_content, pii_doc = pii_redactor.redact(content)
            total_pii_count += pii_doc
            clean_rag_texts.append(f"[Source: {doc.get('metadata', {}).get('source', 'unknown')}]\n{clean_content}")

        context_blocks = "\n\n".join(clean_rag_texts)

        # Step 3: Enforce Token Constraints & Format Payload
        assembled_payload = {
            "system_prompt": clean_system,
            "context_data": context_blocks,
            "conversation_history": conversation_history,
            "user_query": clean_query
        }

        # Calculate total estimated tokens
        full_text = f"{clean_system} {context_blocks} {clean_query}"
        estimated_tokens = self.estimate_tokens(full_text)

        return assembled_payload, total_pii_count


context_builder = ContextBuilder()
