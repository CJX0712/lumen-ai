"""评测基准测试：EvalReport / run_rag_eval / run_agent_eval / load_dataset。"""

from lumen.eval import EvalReport, load_dataset, run_agent_eval, run_rag_eval
from lumen.llm import MockLLM
from lumen.multimodal import MockVision


def test_eval_report_accuracy():
    r = EvalReport("rag", cases=4, passed=3)
    assert r.accuracy == 0.75
    assert "3/4" in str(r)
    d = r.to_dict()
    assert d["accuracy"] == 0.75


def test_eval_report_empty():
    r = EvalReport("x", cases=0, passed=0)
    assert r.accuracy == 0.0


def test_load_dataset(tmp_path):
    p = tmp_path / "qa.json"
    p.write_text('[{"question":"q","expect":"e"}]', encoding="utf-8")
    data = load_dataset(str(p))
    assert data[0]["question"] == "q"


def test_run_rag_eval(container, tmp_path):
    doc = tmp_path / "doc.txt"
    doc.write_text(
        "Lumen 是模块化的端到端 AI 系统，采用 RAG 检索增强架构。",
        encoding="utf-8",
    )
    # 让 Mock LLM 的回答包含期望关键词
    container.override("llm", MockLLM(reply="Lumen 采用模块化 RAG 架构"))
    container.rag().ingest(str(doc))
    qa = [{"question": "Lumen 是什么", "expect": "模块化"}]
    report = run_rag_eval(container.rag(), qa)
    assert report.cases == 1
    assert report.passed == 1
    assert report.details[0]["answer_ok"] is True
    assert report.details[0]["retrieval_hit"] is True


def test_run_agent_eval(container):
    # 默认 fixture llm 固定返回 "42"，智能体轨迹中含该字符串
    report = run_agent_eval(container.agent(), [{"question": "1+1?", "expect": "42"}])
    assert report.cases == 1
    assert report.passed == 1


def test_run_agent_eval_with_final_answer(container):
    container.override(
        "llm", MockLLM(replies=["Final Answer: 答案是 60"])
    )
    report = run_agent_eval(container.agent(), [{"question": "算 (12+8)*3", "expect": "60"}])
    assert report.passed == 1
