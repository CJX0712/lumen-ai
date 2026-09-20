"""集中配置与依赖注入容器。

所有模块经由 Container 按配置组装为可运行链路；测试可调用
``container.override(name, instance)`` 注入 Mock 实现，做到各模块独立验证。
"""

from __future__ import annotations

from functools import lru_cache
from typing import Any, Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """运行配置，支持环境变量 (前缀 LUMEN_) 与 .env 文件覆盖。"""

    model_config = SettingsConfigDict(env_prefix="LUMEN_", env_file=".env", extra="ignore")

    # LLM 后端：ollama | openai | mock
    llm_backend: str = "ollama"
    ollama_host: str = "http://localhost:11434"
    ollama_model: str = "llama3.2:1b"

    # 嵌入后端：ollama | mock
    embed_backend: str = "ollama"
    ollama_embed_model: str = "nomic-embed-text"
    embed_dim: int = 768

    # OpenAI 兼容后端
    openai_api_key: str = ""
    openai_base_url: str = "https://api.openai.com/v1"
    openai_model: str = "gpt-4o-mini"

    # 检索 / 分块
    vectorstore_path: str = "./data/vectorstore"
    chunk_size: int = 500
    chunk_overlap: int = 50
    top_k: int = 4

    # 智能体
    max_agent_steps: int = 6
    log_level: str = "INFO"


@lru_cache
def get_settings() -> Settings:
    return Settings()


class Container:
    """轻量依赖注入容器：按单一职责构建并缓存各模块单例。"""

    def __init__(self, settings: Optional[Settings] = None):
        self.settings = settings or get_settings()
        self._cache: dict[str, Any] = {}

    def override(self, name: str, instance: Any) -> None:
        """测试 / 自定义装配时覆盖某个模块实例。"""
        self._cache[name] = instance

    def llm(self):
        if "llm" not in self._cache:
            from .llm import build_llm

            self._cache["llm"] = build_llm(self.settings)
        return self._cache["llm"]

    def embedder(self):
        if "embedder" not in self._cache:
            from .embeddings import build_embedder

            self._cache["embedder"] = build_embedder(self.settings)
        return self._cache["embedder"]

    def vectorstore(self):
        if "vectorstore" not in self._cache:
            from .vectorstore import build_vectorstore

            self._cache["vectorstore"] = build_vectorstore(self.settings)
        return self._cache["vectorstore"]

    def memory(self):
        if "memory" not in self._cache:
            from .memory import ConversationMemory

            self._cache["memory"] = ConversationMemory()
        return self._cache["memory"]

    def tools(self):
        if "tools" not in self._cache:
            from .tools import build_registry

            self._cache["tools"] = build_registry()
        return self._cache["tools"]

    def rag(self):
        if "rag" not in self._cache:
            from .rag import RAG

            self._cache["rag"] = RAG(
                self.embedder(),
                self.vectorstore(),
                self.llm(),
                self.settings.chunk_size,
                self.settings.chunk_overlap,
                self.settings.top_k,
            )
        return self._cache["rag"]

    def agent(self):
        if "agent" not in self._cache:
            from .agent import Agent

            self._cache["agent"] = Agent(
                self.llm(), self.tools(), self.memory(), self.settings.max_agent_steps
            )
        return self._cache["agent"]
