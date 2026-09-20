"""文档摄入模块入口。"""

from __future__ import annotations

from .chunker import chunk_documents, chunk_text
from .loader import Document, load_file

__all__ = ["Document", "load_file", "chunk_text", "chunk_documents"]
