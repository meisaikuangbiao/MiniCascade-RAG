# MiniCascade-RAG

Reasoning RAG

## Quick Start

```bash
cd docker
cp .env.example .env
docker compose up -d
```

### Deployment
#### 3.1 uv environment
Enter project directory, use：
```bash
uv sync   # if not have uv use "pip install uv" for install
``` 
to synchronize project environment automatically

#### 3.2 docker
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

## API KEY Configure

All the sensitive credentials are placed in a `.env` file that will always sit at the root of your directory, at the same level with the `.env.example` file.

Go to the root of the repository and copy our `.env.example` file as follows:
```shell
cp .env.example .env
```
Now fill it with your credentials, following the suggestions from the next section.
