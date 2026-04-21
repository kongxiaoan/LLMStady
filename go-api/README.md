# go-api

这是当前仓库中为 `Python Agent + Go gRPC API` 方案准备的 Go API 工程。

## 设计目标

- 对外暴露稳定的 gRPC 契约
- 使用 DDD 分层组织代码
- 使用 MySQL 持久化会话记录
- 使用 Redis 做缓存与短期加速
- 通过内部 `AgentClient` 调用 Python Agent 服务

## 目录结构

```text
go-api
├── cmd/server                    # 程序启动入口
├── gen/proto                     # protoc 生成代码
├── internal
│   ├── application               # 应用层：编排用例
│   ├── domain                    # 领域层：实体、值对象、仓储接口
│   ├── infrastructure            # 基础设施层：MySQL / Redis / HTTP Client
│   └── interfaces/grpc           # 接口层：gRPC Handler 与 Server
├── proto                         # protobuf 契约
└── .env.example                  # 本地配置示例
```

## 快速开始

1. 复制配置：

```bash
cp .env.example .env
```

2. 生成 protobuf 代码：

```bash
make proto
```

3. 拉取依赖：

```bash
make tidy
```

4. 运行服务：

```bash
make run
```

## 当前状态说明

当前工程已经具备：

- gRPC 服务入口
- DDD 分层骨架
- MySQL / Redis 基础设施封装
- Python Agent 的 HTTP Client 抽象
- 会话记录持久化接口

后续你可以继续做：

1. 给 Python Agent 增加 HTTP 服务入口
2. 补会话表迁移
3. 把 `AskExpert` 逻辑接通真实 Python Agent
4. 增加鉴权、日志、链路追踪、限流
