from lumen.config import Container, Settings, get_settings


def test_defaults():
    s = Settings()
    assert s.llm_backend == "ollama"
    assert s.embed_dim == 768
    assert s.top_k == 4


def test_env_override(monkeypatch):
    monkeypatch.setenv("LUMEN_LLM_BACKEND", "openai")
    monkeypatch.setenv("LUMEN_OPENAI_API_KEY", "sk-test")
    s = Settings()
    assert s.llm_backend == "openai"
    assert s.openai_api_key == "sk-test"


def test_container_override():
    c = Container(Settings(llm_backend="mock"))
    c.override("llm", object())
    assert c.llm() is c.llm()  # 单例缓存


def test_get_settings_cached():
    assert get_settings() is get_settings()
