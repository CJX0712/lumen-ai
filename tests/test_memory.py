from lumen.memory import ConversationMemory


def test_add_and_context():
    m = ConversationMemory()
    m.add("hi", "hello")
    m.add("bye", "goodbye")
    ctx = m.get_context()
    assert "hi" in ctx and "hello" in ctx


def test_window_truncates():
    m = ConversationMemory(window=2)
    for i in range(5):
        m.add(f"u{i}", f"a{i}")
    ctx = m.get_context()
    assert "u0" not in ctx
    assert "u4" in ctx


def test_clear():
    m = ConversationMemory()
    m.add("x", "y")
    m.clear()
    assert m.get_context() == ""
