import numpy as np
from typing import List


class EmbeddingGenerator:
    """Mock Vector Embedding Generator for Enterprise Pipeline."""

    def generate_embedding(self, text: str, dimension: int = 384) -> List[float]:
        # Generate normalized pseudo-random vector based on text hash seed
        seed = sum(ord(c) for c in text) % (2**32)
        rng = np.random.default_rng(seed)
        vec = rng.standard_normal(dimension)
        normalized_vec = vec / np.linalg.norm(vec)
        return normalized_vec.tolist()


embedding_generator = EmbeddingGenerator()
