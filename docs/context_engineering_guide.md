# Enterprise Context Engineering Guide

## Best Practices for Enterprise GenAI Context Construction

Context Engineering goes beyond basic prompt engineering by programmatically optimizing the dynamic context payload supplied to LLMs.

### 1. Token Budget Allocation Strategies

A standard enterprise prompt context consists of 4 main sections:

| Section | Recommended Budget % | Purpose |
|---------|---------------------|---------|
| **System Prompt & Rules** | 15% - 20% | Security constraints, tone, output format schema |
| **Retrieved Context (RAG)** | 50% - 60% | Grounding facts from internal knowledge bases |
| **Conversation History** | 15% - 20% | Sliding window of recent interactions |
| **User Query & Guardrails** | 5% - 10% | Active user input |

### 2. Semantic Chunking Guidelines

- **Chunk Size**: Standard range of 250 to 500 words (or 350 - 700 tokens).
- **Overlap**: Maintain 10-15% overlap between adjacent chunks to prevent entity loss across boundary lines.
- **Metadata Enriched Headers**: Prefix chunks with document metadata (title, author, updated date, access clearance) before vector indexing.

### 3. PII Redaction Policies

Always sanitize input and context prior to LLM submission:
- Replace email addresses with `[REDACTED_EMAIL]`.
- Replace social security numbers with `[REDACTED_SSN]`.
- Replace API keys/passwords with `[REDACTED_SECRET]`.
