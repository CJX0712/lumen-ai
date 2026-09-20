#!/usr/bin/env bash
# Lumen AI 一键安装脚本（Linux / macOS）。Windows 请用 PowerShell 等价命令。
set -euo pipefail

echo "==> 创建虚拟环境"
python -m venv .venv
# shellcheck disable=SC1091
source .venv/bin/activate

echo "==> 升级 pip 并安装项目（含开发依赖）"
pip install --upgrade pip
pip install -e ".[dev]"

echo ""
echo "==> 安装完成"
echo "可选：安装 Ollama 并拉取模型，以启用本地真实推理："
echo "  macOS/Linux:  brew install ollama && ollama pull llama3.2:1b && ollama pull nomic-embed-text"
echo "  Windows:      从 https://ollama.com 安装桌面版，然后 ollama pull llama3.2:1b"
echo ""
echo "运行："
echo "  make serve      # API 服务 :8000"
echo "  make web        # Gradio 界面 :7860"
echo "  make test       # 单元测试"
