"""可观测性测试：指标采集、单例、LLM 指标包装器。"""

from lumen.llm import MockLLM
from lumen.llm.base import Message
from lumen.observability import (
    Metrics,
    MetricsWrapper,
    get_metrics,
    reset_metrics,
)
from lumen.observability.metrics import _global


def test_metrics_record_and_snapshot():
    m = Metrics()
    m.record("llm", 0.1)
    m.record("llm", 0.3, error=True, tokens_in=10, tokens_out=20)
    snap = m.snapshot()
    assert snap["calls"] == 2
    assert snap["errors"] == 1
    assert snap["tokens_in"] == 10
    assert snap["tokens_out"] == 20
    # 0.1s + 0.3s = 0.4s 平均 0.2s = 200ms
    assert 199 < snap["avg_latency_ms"] < 201
    assert snap["per_module"]["llm"]["calls"] == 2


def test_metrics_reset():
    m = Metrics()
    m.record("llm", 0.1)
    m.reset()
    assert m.snapshot()["calls"] == 0


def test_get_metrics_is_singleton():
    a = get_metrics()
    b = get_metrics()
    assert a is b is _global


def test_metrics_wrapper_records_calls():
    reset_metrics()
    inner = MockLLM(reply="hello world")
    wrapped = MetricsWrapper(inner, module="llm")
    out = wrapped.complete("ping")
    assert out == "hello world"
    snap = get_metrics().snapshot()
    assert snap["calls"] == 1
    assert snap["errors"] == 0
    assert snap["tokens_out"] > 0  # 近似 token 计费


def test_metrics_wrapper_records_error():
    reset_metrics()

    class BoomLLM(MockLLM):
        def complete(self, prompt, *, system=None, **kwargs):
            raise RuntimeError("boom")

    wrapped = MetricsWrapper(BoomLLM(), module="llm")
    try:
        wrapped.complete("x")
    except RuntimeError:
        pass
    snap = get_metrics().snapshot()
    assert snap["calls"] == 1
    assert snap["errors"] == 1


def test_metrics_wrapper_chat_records():
    reset_metrics()
    wrapped = MetricsWrapper(MockLLM(reply="ok"), module="llm")
    wrapped.chat([Message.user("hi")])
    assert get_metrics().snapshot()["calls"] == 1
