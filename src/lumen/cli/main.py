"""命令行入口 (typer)。"""

from __future__ import annotations

import json
import subprocess
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


@app.command("rag-ingest-image")
def rag_ingest_image(path: str = typer.Argument(..., help="图片路径 (png/jpg)")):
    """用视觉模型为图片生成描述并摄入 RAG（多模态摄入）。"""
    n = _container().rag().ingest_image(path)
    typer.echo(f"图片已摄入 {n} 块")


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


@app.command("vision")
def vision(path: str = typer.Argument(..., help="图片路径")):
    """用视觉语言模型描述图片内容。"""
    typer.echo(_container().vision().caption(path))


@app.command("eval")
def evaluate(
    rag_dataset: str = typer.Option(None, "--rag", help="RAG 评测数据集 JSON 路径"),
    agent_dataset: str = typer.Option(None, "--agent", help="智能体评测数据集 JSON 路径"),
):
    """运行评测基准，打印准确率报告。"""
    from ..eval import load_dataset, run_agent_eval, run_rag_eval

    c = _container()
    if rag_dataset:
        report = run_rag_eval(c.rag(), load_dataset(rag_dataset))
        typer.echo(str(report))
    if agent_dataset:
        report = run_agent_eval(c.agent(), load_dataset(agent_dataset))
        typer.echo(str(report))
    if not rag_dataset and not agent_dataset:
        typer.echo("请提供 --rag 或 --agent 评测数据集路径。")


@app.command("models")
def models_pull(
    models: list[str] = typer.Argument(
        None, help="要拉取的模型列表（默认 llama3.2:1b nomic-embed-text llava）"
    ),
):
    """拉取 Ollama 模型（真实推理前准备）。"""
    targets = models or ["llama3.2:1b", "nomic-embed-text", "llava"]
    for m in targets:
        typer.echo(f"拉取 {m} ...")
        subprocess.run(["ollama", "pull", m], check=False)


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
