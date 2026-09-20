"""Lumen · 模块化端到端可运行 AI 系统。

单一职责模块：config / llm / embeddings / vectorstore / ingest / rag /
memory / tools / agent / api / cli / ui。每个模块含抽象接口 + 具体实现，
可独立验证并协同组成完整可运行链路。
"""

from .config import Container, Settings, get_settings

__version__ = "0.1.0"
__author__ = "晨星"
