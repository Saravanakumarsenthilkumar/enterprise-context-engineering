import re
from typing import Tuple, Optional


class InputGuardrails:
    def __init__(self):
        self.injection_patterns = [
            r"ignore\s+all\s+previous\s+instructions",
            r"system\s+prompt\s+override",
            r"you\s+are\s+now\s+DAN",
            r"bypass\s+security\s+filter"
        ]

    def validate_prompt(self, user_prompt: str) -> Tuple[bool, Optional[str]]:
        """Checks user input for prompt injection attack vectors."""
        for pattern in self.injection_patterns:
            if re.search(pattern, user_prompt, re.IGNORECASE):
                return False, f"Prompt injection pattern detected: '{pattern}'"

        if len(user_prompt.strip()) == 0:
            return False, "Prompt cannot be empty"

        return True, None


guardrails = InputGuardrails()
