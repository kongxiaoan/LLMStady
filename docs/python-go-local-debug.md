# Python Agent + Go gRPC 本地联调指南

这份文档描述当前仓库里两层服务如何本地联调：

- Python Agent HTTP 服务
- Go gRPC API 服务

目标架构：

```text
grpc client
   ->
Go gRPC API (:50051)
   ->
Python Agent HTTP (:8080)
   ->
DeepSeek / Tools / Memory
```

---

## 一、启动 Python Agent HTTP 服务

在仓库根目录执行：

```bash
source .llm/bin/activate
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

---

## 二、准备 Go API 配置

复制配置文件：

```bash
cp go-api/.env.example go-api/.env
```

关键配置：

```env
GRPC_ADDR=:50051
PYTHON_AGENT_BASE_URL=http://127.0.0.1:8080
MYSQL_DSN=root:password@tcp(127.0.0.1:3306)/mobile_architect?charset=utf8mb4&parseTime=True&loc=Local
REDIS_ADDR=127.0.0.1:6379
```

说明：

- `PYTHON_AGENT_BASE_URL` 必须指向上面启动的 Python 服务
- Go API 启动时会连接 MySQL 和 Redis

---

## 三、启动 Go gRPC 服务

进入 Go 项目目录：

```bash
cd go-api
```

运行：

```bash
make run
```

默认监听：

```text
:50051
```

---

## 四、用 grpcurl 调试

当前 Go gRPC 服务开启了 reflection，可以直接用 `grpcurl` 调：

```bash
grpcurl -plaintext localhost:50051 list
```

请求示例：

```bash
grpcurl -plaintext \
  -d '{
    "question": "请帮我分析 Android 首页启动优化路径",
    "threadId": "local-debug-thread",
    "userName": "Zhuanz",
    "targetPlatform": "android",
    "experienceLevel": "intermediate",
    "preferredLanguage": "java"
  }' \
  localhost:50051 \
  mobile_architect.v1.MobileArchitectService/AskExpert
```

---

## 五、排查顺序建议

如果联调失败，建议按这个顺序排查：

1. 先检查 Python 健康接口：

```bash
curl http://127.0.0.1:8080/healthz
```

2. 再检查 Go 配置中的 `PYTHON_AGENT_BASE_URL`
3. 再检查 MySQL / Redis 是否已启动
4. 最后再用 `grpcurl` 调 gRPC 接口

---

## 六、VS Code 调试建议

当前仓库已经可以分别调试：

- Python Agent 主程序
- Python HTTP API
- Go gRPC API

推荐联调顺序：

1. 先启动 `Python: 调试 llm-api HTTP 服务`
2. 再启动 `Go: 调试 gRPC API`
3. 最后用 `grpcurl` 或客户端调 gRPC

---

## 七、当前仓库中的联调测试

目前已经有两类测试：

1. Python HTTP 层测试
   文件：[tests/test_http_app.py](/Users/Zhuanz/android/llm/tests/test_http_app.py:1)

2. Go HTTP Client / 应用服务测试
   文件：
   [go-api/internal/infrastructure/agent/http_client_test.go](/Users/Zhuanz/android/llm/go-api/internal/infrastructure/agent/http_client_test.go:1)
   [go-api/internal/application/service/mobile_architect_service_test.go](/Users/Zhuanz/android/llm/go-api/internal/application/service/mobile_architect_service_test.go:1)

这些测试能帮助你确认：

- Python HTTP 协议有没有变
- Go 调 Python 的字段映射有没有坏
- Go 应用层缓存与持久化编排是否正常
