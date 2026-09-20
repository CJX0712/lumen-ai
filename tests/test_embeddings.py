import math

from lumen.embeddings import MockEmbedder


def test_dim():
    assert MockEmbedder(dim=16).dim == 16


def test_deterministic():
    e = MockEmbedder(dim=8)
    a = e.embed(["hello"])
    b = e.embed(["hello"])
    assert a == b


def test_normalized():
    e = MockEmbedder(dim=8)
    vec = e.embed(["world"])[0]
    assert len(vec) == 8
    norm = math.sqrt(sum(v * v for v in vec))
    assert abs(norm - 1.0) < 1e-9


def test_batch():
    e = MockEmbedder(dim=4)
    out = e.embed(["a", "b", "c"])
    assert len(out) == 3
    assert all(len(v) == 4 for v in out)
