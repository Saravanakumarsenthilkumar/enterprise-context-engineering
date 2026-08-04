from typing import List, Dict, Any


class TextChunker:
    def __init__(self, chunk_size: int = 300, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split_text(self, text: str, metadata: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        words = text.split()
        if not words:
            return []

        chunks = []
        step = max(1, self.chunk_size - self.chunk_overlap)
        
        for i in range(0, len(words), step):
            chunk_words = words[i:i + self.chunk_size]
            chunk_text = " ".join(chunk_words)
            chunk_doc = {
                "content": chunk_text,
                "metadata": metadata or {},
                "chunk_index": len(chunks)
            }
            chunks.append(chunk_doc)
            if i + self.chunk_size >= len(words):
                break

        return chunks


text_chunker = TextChunker()
