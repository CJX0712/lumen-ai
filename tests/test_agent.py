from lumen.llm import MockLLM


def test_agent_uses_tool(container):
    # 第一轮产出 Action，第二轮产出 Final Answer
    llm = MockLLM(
        replies=[
            "Thought: 需要计算\nAction: calculator[2+3]",
            "Final Answer: 结果是 5",
        ]
    )
    container.override("llm", llm)
    answer = container.agent().run("1+4 等于几")
    assert "5" in answer


def test_agent_direct_final(container):
    llm = MockLLM(replies=["Final Answer: 直接回答"])
    container.override("llm", llm)
    assert container.agent().run("你好") == "直接回答"


def test_agent_unknown_tool_fallback(container):
    llm = MockLLM(
        replies=[
            "Action: nonexist[x]",
            "Final Answer: 无工具可用",
        ]
    )
    container.override("llm", llm)
    ans = container.agent().run("q")
    assert "无工具可用" in ans
