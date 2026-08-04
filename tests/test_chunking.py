from src.pipeline.chunking import TextChunker


def test_text_chunking():
    chunker = TextChunker(chunk_size=10, chunk_overlap=2)
    sample_text = "Word " * 25
    chunks = chunker.split_text(sample_text, {"doc_id": "test"})

    assert len(chunks) > 1
    assert chunks[0]["metadata"]["doc_id"] == "test"
    assert "Word" in chunks[0]["content"]


def test_empty_chunking():
    chunker = TextChunker()
    chunks = chunker.split_text("")
    assert len(chunks) == 0
