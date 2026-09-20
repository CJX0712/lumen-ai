"""多模态测试：Mock 视觉模型与 build_vision 装配（ollama 仅装配不连网）。"""

from lumen.config import Settings
from lumen.multimodal import MockVision, OllamaVision, VisionLLM, build_vision


def test_mock_vision_caption():
    v = MockVision()
    assert "猫" in v.caption("any.png")
    assert isinstance(v.caption("x"), str)


def test_mock_vision_custom_reply():
    v = MockVision(reply="自定义描述")
    assert v.caption("x") == "自定义描述"


def test_build_vision_mock():
    s = Settings(vision_backend="mock")
    v = build_vision(s)
    assert isinstance(v, MockVision)


def test_build_vision_ollama_assembles():
    s = Settings(vision_backend="ollama", ollama_host="http://localhost:11434")
    v = build_vision(s)
    assert isinstance(v, OllamaVision)
    assert isinstance(v, VisionLLM)
    assert v.model == s.ollama_vision_model


def test_vision_is_abstract():
    import pytest

    with pytest.raises(TypeError):
        VisionLLM()  # 抽象类不可实例化
