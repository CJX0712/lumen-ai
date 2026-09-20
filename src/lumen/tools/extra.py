"""扩展内置工具：联网搜索（DuckDuckGo 即时接口，无需密钥）与受限文件读取。"""

from __future__ import annotations

import os

from .base import BaseTool


class WebSearchTool(BaseTool):
    name = "web_search"
    description = "联网搜索，返回摘要。例如 'web_search[Python GIL]'. 无需 API key。"

    def run(self, inp: str) -> str:
        try:
            import httpx
        except ImportError as e:  # pragma: no cover
            return f"缺少依赖: {e}"
        try:
            resp = httpx.get(
                "https://api.duckduckgo.com/",
                params={"q": inp.strip(), "format": "json", "no_html": 1},
                timeout=10,
                headers={"User-Agent": "lumen/0.1"},
            )
            data = resp.json()
            abstract = data.get("Abstract") or data.get("Answer") or ""
            related = "; ".join(
                r.get("Text", "") for r in data.get("RelatedTopics", [])[:3]
            )
            out = (abstract + " " + related).strip()
            return out or "未找到结果"
        except Exception as e:  # noqa: BLE001
            return f"搜索失败: {e}"


class FileReadTool(BaseTool):
    name = "file_read"
    description = "读取工作目录内的文本文件（防越权）。例如 'file_read[notes.txt]'。"

    def __init__(self, root: str | None = None):
        # 限定可读根目录，默认当前工作目录，防止路径穿越读取敏感文件
        self.root = os.path.abspath(root or os.getcwd())

    def run(self, inp: str) -> str:
        try:
            target = os.path.abspath(os.path.join(self.root, inp.strip()))
            if not target.startswith(self.root + os.sep) and target != self.root:
                return "拒绝访问：超出允许目录"
            if not os.path.isfile(target):
                return f"文件不存在: {inp}"
            with open(target, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()
            return text[:4000] + ("…(截断)" if len(text) > 4000 else "")
        except Exception as e:  # noqa: BLE001
            return f"读取失败: {e}"
