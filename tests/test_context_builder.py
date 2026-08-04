from src.pipeline.context_builder import ContextBuilder


def test_context_builder_pii_redaction():
    builder = ContextBuilder()
    system_prompt = "You are a helpful assistant."
    user_query = "My email is test.user@enterprise.com and SSN is 123-45-6789."
    rag_docs = [
        {"content": "General cloud documentation without PII.", "metadata": {"source": "doc1"}}
    ]

    payload, pii_count = builder.assemble_context(system_prompt, user_query, rag_docs)

    assert pii_count == 2
    assert "[REDACTED_EMAIL]" in payload["user_query"]
    assert "[REDACTED_SSN]" in payload["user_query"]
    assert "test.user@enterprise.com" not in payload["user_query"]
    assert "123-45-6789" not in payload["user_query"]
