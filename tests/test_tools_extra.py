"""扩展工具测试：联网搜索（离线打桩）与受限文件读取（防穿越）。"""

import json

from lumen.tools.extra import FileReadTool, WebSearchTool


class _FakeResp:
    def json(self):
        return {"Abstract": "Python 是一种解释型语言", "RelatedTopics": []}


class _FakeHttpx:
    def get(self, *args, **kwargs):
        return _FakeResp()


def test_web_search_tool(monkeypatch):
    monkeypatch.setattr("httpx.get", _FakeHttpx().get)
    out = WebSearchTool().run("Python")
    assert "Python" in out
    assert isinstance(out, str)


def test_web_search_failure_is_safe(monkeypatch):
    def _boom(*a, **k):
        raise RuntimeError("network down")

    monkeypatch.setattr("httpx.get", _boom)
    out = WebSearchTool().run("x")
    assert "失败" in out  # 异常被捕获，返回友好提示而非崩溃


def test_file_read_reads_file(tmp_path):
    f = tmp_path / "notes.txt"
    f.write_text("Lumen 笔记内容", encoding="utf-8")
    out = FileReadTool(root=str(tmp_path)).run("notes.txt")
    assert "Lumen 笔记内容" in out


def test_file_read_nonexistent(tmp_path):
    out = FileReadTool(root=str(tmp_path)).run("missing.txt")
    assert "不存在" in out


def test_file_read_blocks_parent_traversal(tmp_path):
    tool = FileReadTool(root=str(tmp_path))
    out = tool.run("../secret.txt")
    assert "拒绝访问" in out


def test_file_read_blocks_absolute_outside_root(tmp_path):
    tool = FileReadTool(root=str(tmp_path))
    out = tool.run("/etc/passwd")
    assert "拒绝访问" in out


def test_file_read_truncates_long(tmp_path):
    big = "A" * 5000
    f = tmp_path / "big.txt"
    f.write_text(big, encoding="utf-8")
    out = FileReadTool(root=str(tmp_path)).run("big.txt")
    assert "截断" in out
    assert len(out.replace("…(截断)", "")) <= 4000
