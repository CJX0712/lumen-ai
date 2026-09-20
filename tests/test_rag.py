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


def test_rag_multimodal_ingest_image(container):
    """用 Mock 视觉模型为图片生成描述并摄入 RAG（不依赖 GPU / 网络）。"""
    # 即使图片文件不存在，MockVision 依旧返回确定性描述，验证多模态摄入链路
    n = container.rag().ingest_image("nonexistent.png")
    assert n > 0
    res = container.rag().query("图片里有什么")
    assert isinstance(res["answer"], str)
    assert res["sources"][0]["metadata"].get("type") == "image_caption"
