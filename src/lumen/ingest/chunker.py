"""文本递归分块（按字符窗口 + 重叠）。"""

from __future__ import annotations

from .loader import Document


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    if chunk_size <= 0:
        raise ValueError("chunk_size 必须 > 0")
    if overlap >= chunk_size:
        overlap = chunk_size // 4
    text = text.strip()
    if not text:
        return []

    chunks: list[str] = []
    start = 0
    n = len(text)
    while start < n:
        end = start + chunk_size
        piece = text[start:end].strip()
        if piece:
            chunks.append(piece)
        if end >= n:
            break
        start = end - overlap
    return chunks


def chunk_documents(
    docs: list[Document], chunk_size: int = 500, overlap: int = 50
) -> list[Document]:
    out: list[Document] = []
    for d in docs:
        for i, c in enumerate(chunk_text(d.text, chunk_size, overlap)):
            out.append(
                Document(
                    text=c,
                    source=d.source,
                    metadata={**d.metadata, "chunk": i},
                )
            )
    return out
