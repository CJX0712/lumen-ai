from lumen.tools import (
    CalculatorTool,
    DateTimeTool,
    EchoTool,
    ToolRegistry,
    build_registry,
    safe_calc,
)


def test_safe_calc():
    assert safe_calc("2 + 3 * 4") == 14
    assert safe_calc("(2+3)*4") == 20
    assert safe_calc("2 ** 8") == 256


def test_calculator_tool():
    assert CalculatorTool().run("12+8") == "20"
    assert "错误" in CalculatorTool().run("import os")


def test_datetime_tool():
    assert "UTC" in DateTimeTool().run("")


def test_registry():
    reg = ToolRegistry()
    reg.register(CalculatorTool())
    assert reg.get("calculator") is not None
    assert reg.get("nope") is None
    assert "calculator" in reg.describe()


def test_build_registry_defaults():
    reg = build_registry()
    names = {t.name for t in reg.list()}
    assert names == {"calculator", "datetime", "echo", "web_search", "file_read"}


def test_echo_tool():
    assert EchoTool().run("hi") == "hi"
