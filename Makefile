.PHONY: setup test run serve web freeze clean

setup:  ## 创建虚拟环境并安装含开发依赖的项目
	python -m venv .venv && . .venv/bin/activate && \
	pip install --upgrade pip && pip install -e ".[dev]"

test:  ## 运行全部单元测试（Mock 后端，无需 GPU / 网络）
	pytest -q

run: serve  ## 同 serve

serve:  ## 启动 API 服务 (默认 :8000)
	lumen serve --host 0.0.0.0 --port 8000

web:  ## 启动 Gradio Web 界面 (默认 :7860)
	lumen web --host 0.0.0.0 --port 7860

freeze:  ## 重新生成 requirements.lock.txt
	pip freeze > requirements.lock.txt

clean:  ## 清理运行时数据
	rm -rf data *.faiss .pytest_cache
