# MiniCascade-RAG

Reasoning RAG

## 快速启动

```bash
cd docker
cp .env.example .env
docker compose up -d
```

### 项目部署
#### 3.1 环境部署
进入项目目录，输入：
```bash
uv sync   # 若未安装uv先pip install uv 安装
``` 
自动同步项目环境

#### 3.2 docker 启动
Qdrant：
```bash
docker run -p 6333:6333 -p 6334:6334 \
    -v "$(pwd)/qdrant_storage:/qdrant/storage:z" \
    qdrant/qdrant
```

Rabbitmq
#### latest RabbitMQ 4.x
```bash
docker run -it --rm --name rabbitmq \
    -p 5672:5672 -p 15672:15672 \
    rabbitmq:4-management
```
