"""Ollama 多模态后端（如 llava），把图片转为文本描述。"""

from __future__ import annotations

import base64

from .base import VisionLLM


class OllamaVision(VisionLLM):
    def __init__(self, host: str, model: str, timeout: int = 180):
        try:
            import ollama
        except ImportError as e:  # pragma: no cover
            raise RuntimeError("需要 ollama 包: pip install ollama") from e
        self._client = ollama.Client(host=host, timeout=timeout)
        self.model = model

    def caption(self, image_path: str, prompt: str = "描述这张图片的内容") -> str:
        with open(image_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")
        resp = self._client.generate(model=self.model, prompt=prompt, images=[b64])
        return resp["response"]
