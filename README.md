# llm

一个用于学习 **LangChain v1 + DeepSeek + Agent 工程化设计** 的 Python 项目。

这个项目不是简单的单文件 Demo，而是按真实工程的方式拆成了：

- 配置层
- 领域模型层
- Prompt 层
- Tool 层
- Agent 装配层
- CLI 入口层
- 单元测试

Agent 的定位是：

> 一名专家级移动端工程师，精通 Android / iOS / Flutter / React Native 架构设计、设计模式、Java 六大设计原则、性能优化、代码评审与工程治理。

## 官方选型依据

本项目按 LangChain 当前官方方向实现：

- LangChain v1 推荐使用 `create_agent`
- DeepSeek 官方集成推荐使用 `ChatDeepSeek`
- DeepSeek `deepseek-reasoner` 当前不支持工具调用与结构化输出，因此 Agent 默认使用 `deepseek-chat`

参考资料：

- LangChain v1 发布说明：<https://docs.langchain.com/oss/python/releases/langchain-v1>
- LangChain Agents：<https://docs.langchain.com/oss/python/langchain/agents>
- ChatDeepSeek 集成：<https://docs.langchain.com/oss/python/integrations/chat/deepseek>

## 项目结构

```text
.
├── src/llm         # Python Agent 本体
├── docs            # 学习与架构文档
└── go-api          # Go gRPC API 层（DDD + MySQL + Redis）
```

## 环境准备

激活现有虚拟环境：

```bash
source .llm/bin/activate
```

安装项目依赖：

```bash
pip install -e . --no-build-isolation
```

如果你希望在不同电脑上尽量保持依赖版本一致，推荐先安装锁定版本文件：

```bash
pip install -r requirements.lock.txt
pip install -e . --no-build-isolation
```

说明：

- `pyproject.toml` 负责声明项目依赖和工程入口
- `requirements.lock.txt` 负责固定当前验证通过的一组依赖版本

## 配置 `.env`

```env
DEEPSEEK_API_KEY=你的 DeepSeek Key
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_MODEL=deepseek-chat
APP_TEMPERATURE=0
APP_MAX_RETRIES=2
APP_DEFAULT_THREAD_ID=mobile-architect-thread
APP_DEBUG=false
APP_HTTP_HOST=127.0.0.1
APP_HTTP_PORT=8080
```

初始化本地配置：

```bash
cp .env.example .env
```

## 运行方式

推荐方式：

```bash
llm "请帮我设计一个适合大型 Android 项目的架构方案"
```

你也可以带上下文参数：

```bash
llm "我的 Android 首页启动很慢，帮我分析优化路径" \
  --platform android \
  --experience intermediate \
  --language java \
  --thread-id startup-session
```

或用 Python 方式启动：

```bash
python -m llm.main "请解释 Java 六大设计原则在 Android 项目中的落地方式"
```

也支持直接执行文件：

```bash
python src/llm/main.py "如何设计一个可演进的 Flutter 架构"
```

## 新电脑恢复环境

如果你在另一台电脑上下载这个项目，推荐按下面步骤恢复：

```bash
pyenv install 3.14.4
pyenv local 3.14.4
python -m venv .llm
source .llm/bin/activate
pip install -U pip
pip install -r requirements.lock.txt
pip install -e . --no-build-isolation
cp .env.example .env
```

然后补上你自己的：

- `DEEPSEEK_API_KEY`
- `LANGSMITH_API_KEY`（如果你启用了 LangSmith）

## HTTP 服务入口

如果你要让 Go API 层调用当前 Python Agent，可以启动 HTTP 服务：

```bash
llm-api
```

默认监听：

```text
127.0.0.1:8080
```

健康检查：

```bash
curl http://127.0.0.1:8080/healthz
```

请求示例：

```bash
curl -X POST http://127.0.0.1:8080/v1/mobile-architect/ask \
  -H "Content-Type: application/json" \
  -d '{
    "question": "请帮我设计一个适合大型 Android 项目的架构方案",
    "thread_id": "demo-thread",
    "user_name": "Zhuanz",
    "target_platform": "android",
    "experience_level": "intermediate",
    "preferred_language": "java"
  }'
```

## 测试

```bash
python -m unittest discover -s tests -v
```

如果你当前环境无法访问外网，`pip install -e .` 可能会因为默认隔离构建去拉取构建依赖而失败。
因此这里默认推荐使用 `--no-build-isolation`。

Go 测试：

```bash
cd go-api
go test ./...
```

## 学习建议

建议你按这个顺序阅读源码：

1. [config.py](./src/llm/config.py)
2. [domain/models.py](./src/llm/domain/models.py)
3. [tools/](./src/llm/tools)
4. [agent/factory.py](./src/llm/agent/factory.py)
5. [cli.py](./src/llm/cli.py)

这样你会更容易理解：

- LangChain `create_agent` 怎么组织
- `context_schema` 有什么工程价值
- `response_format` 为什么适合工程化输出
- 为什么项目要把 Tool、Prompt、配置拆层

## 文档

- [Python 模块真实加载顺序](./docs/python-module-loading-flow.md)
- [LangGraph Server 是什么](./docs/langgraph-server.md)
- [Python Agent + Go gRPC API 分层设计建议](./docs/go-grpc-api-architecture.md)
- [Python Agent + Go gRPC 本地联调指南](./docs/python-go-local-debug.md)

## Go API 层

仓库中的 [go-api](./go-api) 是后续服务化演进使用的 Go 工程，职责是：

- 对外暴露 gRPC 契约
- 作为 Python Agent 的 API 网关层
- 使用 MySQL 持久化会话记录
- 使用 Redis 做缓存
- 按 DDD 分层组织代码

初始化 Go 工程：

```bash
cp go-api/.env.example go-api/.env
cd go-api
make proto
make tidy
```

启动 Go gRPC API：

```bash
make run
```

本地联调建议顺序：

1. 先启动 Python HTTP 服务 `llm-api`
2. 再启动 Go gRPC API
3. 最后用 `grpcurl` 或客户端调试
