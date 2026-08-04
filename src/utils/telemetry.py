import time
from typing import Dict, Any
from src.utils.logger import get_logger

logger = get_logger("telemetry")


class MetricsCollector:
    def __init__(self):
        self.metrics: Dict[str, Any] = {
            "total_requests": 0,
            "total_tokens_processed": 0,
            "pii_redactions_count": 0,
            "blocked_requests": 0
        }

    def record_context_assembly(self, token_count: int, pii_count: int, latency_ms: float):
        self.metrics["total_requests"] += 1
        self.metrics["total_tokens_processed"] += token_count
        self.metrics["pii_redactions_count"] += pii_count
        logger.info(
            "context_assembly_metrics",
            extra={
                "tokens": token_count,
                "pii_redactions": pii_count,
                "latency_ms": round(latency_ms, 2)
            }
        )

    def record_blocked_request(self, reason: str):
        self.metrics["blocked_requests"] += 1
        logger.warning("request_blocked", extra={"reason": reason})


metrics_collector = MetricsCollector()
