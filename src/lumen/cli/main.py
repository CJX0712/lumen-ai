"""命令行入口 (typer)。"""

from __future__ import annotations

import uvicorn
import typer

from ..config import Container, get_settings


app = typer.Typer(help="Lumen AI 命令行", no_args_is_help=True)


def _container() -> Container:
    return Container(get_settings())


@app.command()
def chat(message: str = typer.Argument(..., help="用户消息")):
    """单次对话补全。"""
    typer.echo(_container().llm().complete(message))


@app.command("rag-ingest")
def rag_ingest(path: str = typer.Argument(..., help="文档路径 (txt/md/json/pdf)")):
    """摄入文档到向量库。"""
    n = _container().rag().ingest(path)
    typer.echo(f"已入库 {n} 块")


@app.command("rag-query")
def rag_query(question: str = typer.Argument(..., help="问题")):
    """基于已摄入文档检索问答。"""
    res = _container().rag().query(question)
    typer.echo("回答: " + res["answer"])
    for i, s in enumerate(res["sources"], 1):
        snippet = s["text"][:80].replace("\n", " ")
        typer.echo(f"  来源{i} (score={s['score']:.3f}): {snippet}...")


@app.command("agent-run")
def agent_run(question: str = typer.Argument(..., help="问题")):
    """运行 ReAct 智能体（含工具调用）。"""
    typer.echo(_container().agent().run(question))


@app.command()
def serve(host: str = "0.0.0.0", port: int = 8000):
    """启动 FastAPI 服务 (默认 :8000)。"""
    c = _container()
    uvicorn.run(create_app(c), host=host, port=port)


@app.command()
def web(host: str = "0.0.0.0", port: int = 7860):
    """启动 Gradio Web 聊天界面 (默认 :7860)。"""
    from ..ui.app import launch

    launch(_container(), host=host, port=port)


def main() -> None:
    app()


if __name__ == "__main__":
    main()
