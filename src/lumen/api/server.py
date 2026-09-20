"""FastAPI 服务：暴露 chat / rag / agent 能力。

请求模型定义在模块级，避免 future-annotations 下 FastAPI 无法将嵌套模型识别为请求体。
"""

from __future__ import annotations

from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from ..observability import get_metrics


class ChatReq(BaseModel):
    message: str
    system: Optional[str] = None


class RagIngestReq(BaseModel):
    path: str


class RagQueryReq(BaseModel):
    question: str
    top_k: Optional[int] = None


class AgentReq(BaseModel):
    question: str


def create_app(container) -> FastAPI:
    app = FastAPI(title="Lumen AI", version="0.1.0")

    @app.get("/health")
    def health():
        return {"status": "ok", "backend": container.settings.llm_backend}

    @app.get("/metrics")
    def metrics():
        return get_metrics().snapshot()

    @app.post("/chat")
    def chat(req: ChatReq):
        try:
            return {"reply": container.llm().complete(req.message, system=req.system)}
        except Exception as e:  # noqa: BLE001
            raise HTTPException(status_code=500, detail=str(e))

    @app.post("/rag/ingest")
    def rag_ingest(req: RagIngestReq):
        try:
            return {"ingested": container.rag().ingest(req.path)}
        except Exception as e:  # noqa: BLE001
            raise HTTPException(status_code=500, detail=str(e))

    @app.post("/rag/query")
    def rag_query(req: RagQueryReq):
        try:
            return container.rag().query(req.question, req.top_k)
        except Exception as e:  # noqa: BLE001
            raise HTTPException(status_code=500, detail=str(e))

    @app.post("/agent/run")
    def agent_run(req: AgentReq):
        try:
            return {"answer": container.agent().run(req.question)}
        except Exception as e:  # noqa: BLE001
            raise HTTPException(status_code=500, detail=str(e))

    return app
