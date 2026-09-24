FROM python:3.14-slim

WORKDIR /app

# 先装锁定的依赖，利用层缓存
COPY requirements.lock.txt .
RUN pip install --no-cache-dir -r requirements.lock.txt

# 再装项目本体
COPY . .
RUN pip install --no-cache-dir .

EXPOSE 8000 7860

# 默认启动 API 服务；Web 界面可用 `lumen web` 启动
CMD ["sh", "-c", "lumen serve --host 0.0.0.0 --port 8000"]
