"""文档加载：支持 txt / md / json / pdf。"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Document:
    text: str
    source: str
    metadata: dict = field(default_factory=dict)


def load_file(path: str) -> list[Document]:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(path)
    suffix = p.suffix.lower()
    text = p.read_text(encoding="utf-8", errors="ignore")

    if suffix in (".txt", ".md", ".text"):
        return [Document(text=text, source=str(p), metadata={"type": suffix.lstrip(".")})]

    if suffix == ".json":
        data = json.loads(text)
        if isinstance(data, list):
            return [
                Document(
                    text=json.dumps(item, ensure_ascii=False),
                    source=f"{p}#{i}",
                    metadata={"type": "json"},
                )
                for i, item in enumerate(data)
            ]
        return [Document(text=json.dumps(data, ensure_ascii=False), source=str(p), metadata={"type": "json"})]

    if suffix == ".pdf":
        return _load_pdf(p)

    raise ValueError(f"不支持的文件类型: {suffix}")


def _load_pdf(p: Path) -> list[Document]:
    try:
        from pypdf import PdfReader
    except ImportError as e:  # pragma: no cover
        raise RuntimeError("读取 PDF 需要 pypdf: pip install pypdf") from e
    reader = PdfReader(str(p))
    text = "\n".join((page.extract_text() or "") for page in reader.pages)
    return [
        Document(
            text=text,
            source=str(p),
            metadata={"type": "pdf", "pages": len(reader.pages)},
        )
    ]
