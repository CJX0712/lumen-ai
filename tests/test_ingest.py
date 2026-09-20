from lumen.ingest import chunk_documents, chunk_text, load_file


def test_chunk_text_basic():
    text = "a" * 1200
    chunks = chunk_text(text, chunk_size=500, overlap=50)
    assert len(chunks) >= 3
    assert all(len(c) <= 500 for c in chunks)


def test_chunk_text_empty():
    assert chunk_text("   ") == []


def test_chunk_text_overlap_guard():
    chunks = chunk_text("x" * 100, chunk_size=10, overlap=9)
    assert len(chunks) > 1


def test_load_txt(tmp_path):
    p = tmp_path / "doc.txt"
    p.write_text("Lumen 是模块化 AI 系统。", encoding="utf-8")
    docs = load_file(str(p))
    assert len(docs) == 1
    assert "Lumen" in docs[0].text


def test_load_json_list(tmp_path):
    import json

    p = tmp_path / "d.json"
    p.write_text(json.dumps([{"q": 1}, {"q": 2}]), encoding="utf-8")
    docs = load_file(str(p))
    assert len(docs) == 2


def test_chunk_documents(tmp_path):
    p = tmp_path / "doc.txt"
    p.write_text("内容 " * 400, encoding="utf-8")
    docs = load_file(str(p))
    chunks = chunk_documents(docs, chunk_size=200, overlap=20)
    assert len(chunks) > 1
    assert all("chunk" in c.metadata for c in chunks)
