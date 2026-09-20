"""RAG 检索增强管线：编排 ingest → embed → store → retrieve → generate。"""

from __future__ import annotations

import uuid

from ..embeddings.base import BaseEmbedder
from ..llm.base import BaseLLM
from ..vectorstore.base import BaseVectorStore
from ..ingest import chunk_documents, load_file


class RAG:
    def __init__(
        self,
        embedder: BaseEmbedder,
        vectorstore: BaseVectorStore,
        llm: BaseLLM,
        chunk_size: int = 500,
        chunk_overlap: int = 50,
        top_k: int = 4,
        vision: "VisionLLM | None" = None,
    ):
        self.embedder = embedder
        self.vectorstore = vectorstore
        self.llm = llm
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.top_k = top_k
        self._vision = vision

    def _ingest_docs(self, docs: list) -> int:
        chunks = chunk_documents(docs, self.chunk_size, self.chunk_overlap)
        if not chunks:
            return 0
        vectors = self.embedder.embed([c.text for c in chunks])
        items = [
            {
                "id": str(uuid.uuid4()),
                "vector": vectors[i],
                "text": c.text,
                "metadata": c.metadata,
            }
            for i, c in enumerate(chunks)
        ]
        self.vectorstore.upsert(items)
        return len(items)

    def ingest(self, path: str) -> int:
        """加载并分块文档，向量化后写入向量库，返回入库块数。"""
        return self._ingest_docs(load_file(path))

    def ingest_image(self, path: str, vision: "VisionLLM | None" = None) -> int:
        """用视觉模型为图片生成文字描述，再作为文本摄入 RAG（多模态摄入）。"""
        vision = vision or self._vision
        if vision is None:
            raise RuntimeError(
                "未配置 vision 后端（设置 LUMEN_VISION_BACKEND=ollama 并安装 llava）"
            )
        from ..ingest import Document

        caption = vision.caption(path)
        return self._ingest_docs(
            [Document(text=caption, source=path, metadata={"type": "image_caption"})]
        )

    def query(self, question: str, top_k: int | None = None) -> dict:
        """检索相关上下文并生成回答。"""
        top_k = top_k or self.top_k
        qv = self.embedder.embed([question])[0]
        results = self.vectorstore.search(qv, top_k)
        context = "\n\n".join(
            f"[来源 {i + 1}] {r.text}" for i, r in enumerate(results)
        )
        prompt = (
            "基于以下上下文回答问题。若上下文没有答案，请明确说明不知道。\n\n"
            f"上下文:\n{context}\n\n问题: {question}\n\n回答:"
        )
        answer = self.llm.complete(prompt, system="你是严谨的检索问答助手。")
        return {
            "answer": answer,
            "sources": [
                {"text": r.text, "score": r.score, "metadata": r.metadata}
                for r in results
            ],
        }
