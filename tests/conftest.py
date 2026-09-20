"""pytest 公共 fixture：用 Mock 后端装配 Container，无需 GPU / 网络。"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import pytest

from lumen.config import Container, Settings
from lumen.embeddings import MockEmbedder
from lumen.llm import MockLLM
from lumen.multimodal import MockVision
from lumen.vectorstore import FAISSVectorStore


@pytest.fixture
def settings():
    return Settings(
        llm_backend="mock",
        embed_backend="mock",
        embed_dim=8,
        vectorstore_path="./data/test_vectorstore",
        vision_backend="mock",
    )


@pytest.fixture
def container(settings):
    c = Container(settings)
    c.override("llm", MockLLM(reply="42"))
    c.override("embedder", MockEmbedder(dim=8))
    c.override("vectorstore", FAISSVectorStore(dim=8))
    c.override("vision", MockVision())
    return c
