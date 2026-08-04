import re
from typing import Tuple


class PIIRedactor:
    def __init__(self):
        # Regex patterns for common enterprise PII & sensitive secrets
        self.patterns = {
            "EMAIL": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
            "SSN": r"\b\d{3}-\d{2}-\d{4}\b",
            "CREDIT_CARD": r"\b(?:\d[ -]*?){13,16}\b",
            "PHONE": r"\b(?:\+?1[-. ]?)?\(?\d{3}\)?[-. ]?\d{3}[-. ]?\d{4}\b",
            "API_KEY": r"\b(?:sk|pk|api|key)_[a-zA-Z0-9]{20,}\b"
        }

    def redact(self, text: str) -> Tuple[str, int]:
        """Redacts PII from given text. Returns (sanitized_text, redaction_count)."""
        redaction_count = 0
        sanitized_text = text

        for entity_type, pattern in self.patterns.items():
            matches = re.findall(pattern, sanitized_text, flags=re.IGNORECASE)
            if matches:
                redaction_count += len(matches)
                sanitized_text = re.sub(
                    pattern,
                    f"[REDACTED_{entity_type}]",
                    sanitized_text,
                    flags=re.IGNORECASE
                )

        return sanitized_text, redaction_count


pii_redactor = PIIRedactor()
