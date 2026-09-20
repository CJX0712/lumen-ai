#!/usr/bin/env python
"""一键拉取 Lumen 默认 Ollama 模型（真实推理前的准备）。

用法:
    python scripts/bootstrap_models.py                 # 拉取默认三件套
    python scripts/bootstrap_models.py llama3.2:1b      # 仅拉取指定模型
也可通过 CLI: lumen models pull
"""

from __future__ import annotations

import subprocess
import sys

DEFAULT_MODELS = ["llama3.2:1b", "nomic-embed-text", "llava"]


def pull(model: str) -> int:
    print(f"==> 拉取 {model}")
    return subprocess.run(["ollama", "pull", model]).returncode


def main() -> None:
    models = sys.argv[1:] or DEFAULT_MODELS
    rc = 0
    for m in models:
        rc |= pull(m)
    sys.exit(rc)


if __name__ == "__main__":
    main()
