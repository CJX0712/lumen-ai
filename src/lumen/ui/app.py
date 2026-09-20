"""Gradio Web 聊天界面。"""

from __future__ import annotations


def launch(container, host: str = "0.0.0.0", port: int = 7860, share: bool = False) -> None:
    """启动 Gradio 聊天界面，直接调用本地 Agent（无需额外 HTTP 服务）。"""
    try:
        import gradio as gr
    except ImportError as e:  # pragma: no cover
        raise RuntimeError("需要 gradio: pip install gradio") from e

    agent = container.agent()
    # 独立记忆，避免与 CLI/API 共享状态
    from ..memory import ConversationMemory

    agent.memory = ConversationMemory()

    def respond(user_message: str, history: list) -> list:
        bot = agent.run(user_message)
        return history + [[user_message, bot]]

    with gr.Blocks(title="Lumen AI") as demo:
        gr.Markdown("# Lumen AI · 智能体对话")
        chatbot = gr.Chatbot(label="对话")
        msg = gr.Textbox(label="输入", placeholder="问点什么，例如：北京现在几点？12*8+3 等于几？")
        msg.submit(respond, [msg, chatbot], [chatbot])

    demo.launch(server_name=host, server_port=port, share=share)
