"""轻量指标收集器：调用次数 / 延迟 / 错误 / 近似 token 数。线程安全。"""

from __future__ import annotations

import threading
from dataclasses import dataclass, field


class Metrics:
    def __init__(self):
        self._lock = threading.Lock()
        self.calls = 0
        self.errors = 0
        self.total_latency = 0.0
        self.tokens_in = 0
        self.tokens_out = 0
        self.per_module: dict[str, dict] = {}

    def record(
        self,
        module: str,
        latency: float,
        error: bool = False,
        tokens_in: int = 0,
        tokens_out: int = 0,
    ) -> None:
        with self._lock:
            self.calls += 1
            if error:
                self.errors += 1
            self.total_latency += latency
            self.tokens_in += tokens_in
            self.tokens_out += tokens_out
            m = self.per_module.setdefault(
                module, {"calls": 0, "errors": 0, "latency": 0.0}
            )
            m["calls"] += 1
            if error:
                m["errors"] += 1
            m["latency"] += latency

    def snapshot(self) -> dict:
        with self._lock:
            return {
                "calls": self.calls,
                "errors": self.errors,
                "avg_latency_ms": round(self.total_latency / self.calls * 1000, 3)
                if self.calls
                else 0.0,
                "tokens_in": self.tokens_in,
                "tokens_out": self.tokens_out,
                "per_module": {k: dict(v) for k, v in self.per_module.items()},
            }

    def reset(self) -> None:
        with self._lock:
            self.__init__()


_global = Metrics()


def get_metrics() -> Metrics:
    return _global


def reset_metrics() -> None:
    _global.reset()
