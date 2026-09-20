def test_rag_ingest_and_query(container, tmp_path):
    doc = tmp_path / "doc.txt"
    doc.write_text("Lumen 是一个模块化 AI 系统，支持 RAG 检索增强与 ReAct 智能体。", encoding="utf-8")
    n = container.rag().ingest(str(doc))
    assert n > 0
    res = container.rag().query("Lumen 是什么")
    assert "answer" in res
    assert isinstance(res["answer"], str)
    assert len(res["sources"]) >= 1


def test_rag_empty_doc(container, tmp_path):
    doc = tmp_path / "empty.txt"
    doc.write_text("   ", encoding="utf-8")
    assert container.rag().ingest(str(doc)) == 0
