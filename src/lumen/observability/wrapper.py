"""MetricsWrapper：透明包裹任意 BaseLLM，自动记录延迟 / 错误 / 近似 token。"""

from __future__ import annotations

import time

from ..llm.base import BaseLLM, Message
from .metrics import get_metrics


class MetricsWrapper(BaseLLM):
    def __init__(self, inner: BaseLLM, module: str = "llm"):
        self.inner = inner
        self.module = module

    def complete(self, prompt: str, *, system: str | None = None, **kwargs) -> str:
        t = time.time()
        err = False
        out = ""
        try:
            out = self.inner.complete(prompt, system=system, **kwargs)
            return out
        except Exception:  # noqa: BLE001
            err = True
            raise
        finally:
            get_metrics().record(
                self.module,
                time.time() - t,
                error=err,
                tokens_in=max(len(prompt) // 4, 0),
                tokens_out=max(len(out) // 4, 0) if not err else 0,
            )

    def chat(self, messages: list[Message], **kwargs) -> str:
        t = time.time()
        err = False
        out = ""
        try:
            out = self.inner.chat(messages, **kwargs)
            return out
        except Exception:  # noqa: BLE001
            err = True
            raise
        finally:
            get_metrics().record(
                self.module,
                time.time() - t,
                error=err,
                tokens_in=max(sum(len(m.content) for m in messages) // 4, 0),
                tokens_out=max(len(out) // 4, 0) if not err else 0,
            )
