"""评测基准：基于规则的可复现指标（无需 GPU / 网络）。

- RAG 评测：给定 QA（含期望关键词），检查答案是否包含关键词，以及检索是否命中。
- 智能体评测：给定问题 + 期望关键词，检查最终回答是否包含关键词（验证工具调用链路）。
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field


@dataclass
class EvalReport:
    name: str
    cases: int
    passed: int
    details: list = field(default_factory=list)

    @property
    def accuracy(self) -> float:
        return self.passed / self.cases if self.cases else 0.0

    def to_dict(self) -> dict:
        d = asdict(self)
        d["accuracy"] = round(self.accuracy, 4)
        return d

    def __str__(self) -> str:
        return f"[{self.name}] 通过 {self.passed}/{self.cases}  准确率 {self.accuracy:.1%}"


def run_rag_eval(rag, qa: list[dict], top_k: int | None = None) -> EvalReport:
    passed = 0
    details = []
    for item in qa:
        res = rag.query(item["question"], top_k)
        ans = res["answer"]
        expect = str(item.get("expect", "")).lower()
        ok = expect in ans.lower()
        hit = any(
            expect in (s.get("text", "")).lower() for s in res.get("sources", [])
        )
        passed += 1 if ok else 0
        details.append(
            {"question": item["question"], "answer_ok": ok, "retrieval_hit": hit}
        )
    return EvalReport("rag", len(qa), passed, details)


def run_agent_eval(agent, cases: list[dict]) -> EvalReport:
    passed = 0
    details = []
    for item in cases:
        ans = agent.run(item["question"])
        expect = str(item.get("expect", "")).lower()
        ok = expect in ans.lower()
        passed += 1 if ok else 0
        details.append({"question": item["question"], "ok": ok})
    return EvalReport("agent", len(cases), passed, details)


def load_dataset(path: str) -> list[dict]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
