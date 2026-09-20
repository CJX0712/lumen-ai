def test_full_pipeline(container, tmp_path):
    doc = tmp_path / "kb.txt"
    doc.write_text(
        "Lumen 是一个模块化 AI 系统。它支持 RAG 检索增强、ReAct 智能体与可插拔 LLM 后端。",
        encoding="utf-8",
    )
    rag = container.rag()
    n = rag.ingest(str(doc))
    assert n > 0

    res = rag.query("Lumen 支持哪些能力")
    assert "answer" in res and res["sources"]

    # 智能体链路（含工具）独立可运行
    ans = container.agent().run("Lumen 是什么")
    assert isinstance(ans, str) and ans
