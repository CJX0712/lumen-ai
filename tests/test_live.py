"""需要真实 LLM / 嵌入后端的集成测试（默认用 Ollama）。

运行: pytest -m live  （需本机已启动 Ollama 并拉取 llama3.2:1b 与 nomic-embed-text）
Ollama 不可达时自动跳过，保证单测可独立通过。
"""

import pytest

from lumen.config import Container, Settings

pytestmark = pytest.mark.live


def _ollama_reachable(host: str) -> bool:
    try:
        import ollama

        ollama.Client(host=host, timeout=5).list()
        return True
    except Exception:  # noqa: BLE001
        return False


@pytest.fixture
def live_container():
    s = Settings(llm_backend="ollama", embed_backend="ollama")
    if not _ollama_reachable(s.ollama_host):
        pytest.skip("Ollama 不可达，跳过 live 测试")
    return Container(s)


def test_live_chat(live_container):
    out = live_container.llm().complete("用中文简要说：你好")
    assert isinstance(out, str) and out.strip()


def test_live_embed_dim(live_container):
    vec = live_container.embedder().embed(["hello"])
    assert len(vec[0]) == live_container.embedder().dim


def test_live_rag(live_container, tmp_path):
    doc = tmp_path / "d.txt"
    doc.write_text("Lumen 是一个模块化 AI 系统，支持 RAG 与智能体。", encoding="utf-8")
    n = live_container.rag().ingest(str(doc))
    assert n > 0
    res = live_container.rag().query("Lumen 是什么")
    assert res["answer"]
