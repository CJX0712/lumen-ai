# Lumen · 模块化端到端可运行 AI 系统

<p align="center">
  <a href="https://github.com/CJX0712/lumen-ai/actions/workflows/ci.yml"><img src="https://github.com/CJX0712/lumen-ai/actions/workflows/ci.yml/badge.svg" alt="ci"></a>
  <a href="https://github.com/CJX0712/lumen-ai/releases"><img src="https://img.shields.io/github/v/release/CJX0712/lumen-ai?sort=semver" alt="release"></a>
  <img src="https://img.shields.io/badge/author-%E6%99%A8%E6%98%9F-1f6feb" alt="author">
</p>

> 复用业界领先开源成果，按单一职责原则划分 AI 功能模块，可插拔后端、独立验证、协同组成完整可运行链路。
> 作者：**晨星**

Lumen 不是从零自研模型，而是把成熟的开源组件（Ollama / FAISS / FastAPI / Pydantic / Typer / Gradio）用清晰的接口编排成一套 **RAG + Agent + Tools** 的完整 AI 应用平台。每个模块都有抽象接口与具体实现，可用 Mock 后端独立测试，无需 GPU 即可在干净环境中一键复现。

**第二版新增（迈向「世界级」）**：可观测指标（`/metrics` + 透明 LLM 包装）、基于规则的可复现评测基准、多模态图片摄入（Vision→RAG）、扩展工具（联网搜索 / 受限文件读取）、一键模型引导脚本。

---

## 一、系统架构

```
接入层   API 服务(FastAPI)  ·  CLI(typer)  ·  Web(Gradio)
   │
编排层   智能体 Agent (ReAct: 思考→工具→观测→回答)
   │
能力层   RAG 检索增强  ·  工具注册中心  ·  对话记忆  ·  多模态视觉摄入
   │
服务层   LLM 网关  ·  嵌入服务  ·  向量库(FAISS)  ·  视觉语言模型
   │
基础设施  配置 / 依赖注入 (Container)
   │
横切    可观测 (Metrics/日志)  ·  评测基准 (EvalHarness)
```

### 模块划分（单一职责）

| 模块 | 职责 | 关键接口 | 复用开源 |
|------|------|----------|----------|
| `config` | 集中配置 + 依赖注入 | `Settings` / `Container` | pydantic-settings |
| `llm` | LLM 网关，屏蔽后端差异 | `BaseLLM.complete()/chat()` | ollama / openai |
| `embeddings` | 文本向量化 | `BaseEmbedder.embed()` | ollama / Mock |
| `vectorstore` | 向量检索 | `BaseVectorStore.upsert()/search()` | faiss-cpu |
| `ingest` | 文档加载 + 分块 | `load_file()` / `chunk_text()` | 内置(txt/md/json/pdf) |
| `rag` | RAG 管线编排（含多模态摄入） | `RAG.ingest()/ingest_image()/query()` | 组合上述模块 |
| `memory` | 滑动窗口对话记忆 | `BaseMemory.add()/get_context()` | 内置 |
| `tools` | 工具注册与接口 | `BaseTool.run()` + `ToolRegistry` | 内置(计算器/时间/回声/搜索/读文件) |
| `agent` | ReAct 智能体 | `Agent.run()` | 组合 llm/tools/memory |
| `multimodal` | 视觉语言模型（图片→文本） | `VisionLLM.caption()` | ollama(llava) / Mock |
| `observability` | 指标采集 + 结构化日志 | `Metrics` / `MetricsWrapper` / `get_metrics()` | 内置 |
| `eval` | 规则化评测基准 | `run_rag_eval()/run_agent_eval()/EvalReport` | 内置 |
| `api` | FastAPI 服务 | `/chat` `/rag/*` `/agent/run` `/health` `/metrics` | fastapi/uvicorn |
| `cli` | 命令行 | typer 子命令（含 eval/models/vision） | typer |
| `ui` | Gradio Web 界面 | `launch()` | gradio |

**调用关系**：`api/cli/ui → agent → {llm, memory, tools, rag}`；`rag → {ingest, embeddings, vectorstore, llm, multimodal}`；`agent/tools → llm`。所有模块经 `config.Container` 装配，测试可 `container.override()` 注入 Mock。`observability` 通过 `MetricsWrapper` 透明包裹 LLM，零侵入采集延迟/错误/近似 token，并暴露 `/metrics`。

---

## 二、部署指南

### 方式 A：本地（推荐开发）

```bash
# 1. 一键安装（创建 .venv 并装好项目）
bash setup.sh

# 2. 启用本地真实推理（可选，CPU 友好）
#    macOS/Linux:
brew install ollama && ollama pull llama3.2:1b && ollama pull nomic-embed-text
#    Windows: 安装 Ollama 桌面版后执行 ollama pull llama3.2:1b

# 3. 启动
make serve     # API 服务  http://localhost:8000
make web       # Gradio 界面 http://localhost:7860
```

### 方式 B：Docker

```bash
docker build -t lumen-ai .
docker run -p 8000:8000 -p 7860:7860 lumen-ai
```

### 方式 C：云端 / GPU 后端（无需改代码）

设置环境变量切换后端（同接口，零代码改动）：

```bash
export LUMEN_LLM_BACKEND=openai
export LUMEN_OPENAI_API_KEY=sk-xxx
export LUMEN_OPENAI_BASE_URL=https://your-endpoint/v1   # 兼容 /v1 的自托管或云
export LUMEN_OPENAI_MODEL=your-model
```

### 可复现性保证

- `pyproject.toml` 声明依赖范围；`requirements.lock.txt` 为 `pip freeze` 锁定的精确版本。
- `.github/workflows/ci.yml` 在 GitHub Actions 上真装 Ollama、拉取小模型并跑集成测试，作为可复现的硬证明。
- `Makefile` / `setup.sh` 提供一键 `setup / test / serve / web / freeze`。

---

## 三、使用指南

### 命令行（CLI）

```bash
lumen chat "用中文介绍一下 RAG"
lumen rag-ingest ./docs/intro.txt        # 文档入向量库
lumen rag-query "Lumen 支持哪些能力"      # 基于文档检索问答
lumen agent-run "12*8+3 等于几？现在北京时间?"  # 智能体调用工具
lumen rag-ingest-image ./photo.png       # 多模态：图片→描述→入 RAG
lumen vision ./photo.png                 # 用视觉模型描述图片
lumen models pull                        # 一键拉取默认 Ollama 模型
lumen eval --rag ./samples/rag_qa.json   # 运行 RAG 评测基准
lumen eval --agent ./samples/agent_qa.json  # 运行智能体评测基准
lumen serve                              # 启动 API :8000（含 /metrics）
lumen web                                # 启动 Web :7860
```

### HTTP API

```bash
curl -X POST localhost:8000/chat -H 'Content-Type: application/json' \
  -d '{"message":"你好"}'

curl -X POST localhost:8000/rag/ingest -H 'Content-Type: application/json' \
  -d '{"path":"./docs/intro.txt"}'

curl -X POST localhost:8000/rag/query -H 'Content-Type: application/json' \
  -d '{"question":"Lumen 是什么"}'

curl -X POST localhost:8000/agent/run -H 'Content-Type: application/json' \
  -d '{"question":"计算 (12+8)*3"}'

curl localhost:8000/metrics              # 可观测：调用次数/延迟/错误/近似 token
```

### Python SDK

```python
from lumen.config import Container, Settings

c = Container(Settings(llm_backend="mock"))   # 或 ollama / openai
print(c.llm().complete("你好"))
print(c.agent().run("计算 2**10"))
```

### 评测基准（可复现）

`lumen.eval` 提供基于规则的可复现评测：给定 QA（含期望关键词），检查答案是否命中关键词、检索是否命中上下文。

```python
from lumen.config import Container, Settings
from lumen.eval import load_dataset, run_rag_eval

c = Container(Settings(llm_backend="mock"))
report = run_rag_eval(c.rag(), load_dataset("./samples/rag_qa.json"))
print(report)            # [rag] 通过 5/5  准确率 100.0%
print(report.to_dict())  # 含 accuracy / details
```

样例数据集位于 `samples/rag_qa.json` 与 `samples/agent_qa.json`，可自由扩展。

### 测试

```bash
pytest -q                 # 单元测试（Mock 后端，无需 GPU）
pytest -m live            # 真实后端集成测试（需 Ollama）
```

---

## 四、扩展指引

- **新增 LLM 后端**：继承 `lumen.llm.BaseLLM` 实现 `complete/chat`，在 `build_llm` 注册。
- **新增工具**：继承 `lumen.tools.BaseTool` 实现 `run()`，用 `registry.register()` 注册即可被智能体调用。
- **新增向量库**：继承 `lumen.vectorstore.BaseVectorStore`，在 `build_vectorstore` 切换。
- **新增视觉模型**：继承 `lumen.multimodal.VisionLLM` 实现 `caption()`，在 `build_vision` 注册，即可接入 `RAG.ingest_image()` 多模态摄入。
- **接入可观测**：Metrics 经 `MetricsWrapper` 自动采集，无需改业务代码；也可直接 `from lumen.observability import get_metrics` 读取/上报。

---

## 许可证与署名

MIT License · 作者 **晨星**
