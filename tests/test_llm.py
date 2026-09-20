from lumen.llm import LLMError, Message, MockLLM


def test_mock_fixed_reply():
    llm = MockLLM(reply="hi")
    assert llm.complete("anything") == "hi"
    assert llm.chat([Message.user("x")]) == "hi"


def test_mock_echo():
    llm = MockLLM(echo=True)
    assert llm.complete("abc") == "[mock]abc"


def test_mock_replies_queue():
    llm = MockLLM(replies=["first", "second"])
    assert llm.complete("a") == "first"
    assert llm.complete("b") == "second"
    assert "Final Answer" in llm.complete("c")


def test_message_helpers():
    assert Message.system("s").role == "system"
    assert Message.user("u").content == "u"
