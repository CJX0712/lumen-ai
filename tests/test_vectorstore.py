from lumen.vectorstore import FAISSVectorStore


def _vs():
    vs = FAISSVectorStore(dim=3)
    vs.upsert(
        [
            {"id": "a", "vector": [1.0, 0.0, 0.0], "text": "alpha", "metadata": {"i": 0}},
            {"id": "b", "vector": [0.0, 1.0, 0.0], "text": "beta", "metadata": {"i": 1}},
            {"id": "c", "vector": [0.0, 0.0, 1.0], "text": "gamma", "metadata": {"i": 2}},
        ]
    )
    return vs


def test_count_and_search():
    vs = _vs()
    assert vs.count() == 3
    results = vs.search([0.9, 0.1, 0.0], top_k=1)
    assert results[0].text == "alpha"


def test_search_returns_sorted_by_score():
    vs = _vs()
    results = vs.search([0.0, 0.0, 1.0], top_k=3)
    assert results[0].text == "gamma"
    assert [r.score for r in results] == sorted(r.score for r in results)


def test_empty_search():
    vs = FAISSVectorStore(dim=2)
    assert vs.search([1, 2], top_k=4) == []


def test_save_load(tmp_path):
    vs = _vs()
    path = str(tmp_path / "vs.pkl")
    vs.save(path)
    vs2 = FAISSVectorStore(dim=3)
    vs2.load(path)
    assert vs2.count() == 3
    assert vs2.search([0.0, 1.0, 0.0], top_k=1)[0].text == "beta"
