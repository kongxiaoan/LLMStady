# Android（LLMClient）与 go-api、Python 联调说明

本文说明仓库内 **go-api**（Go gRPC 网关）如何启动、**Python `llm-api`**（Agent HTTP 服务）如何配置，以及 **LLMClient** Android 工程如何基于 **Retrofit + OkHttp + Kotlin 协程** 完成端到端 Demo。

## 整体架构

```text
┌──────────────────────────────────────────────────────────────┐
│  手机 / 模拟器  LLMClient (Retrofit, HTTP/JSON)                    │
└────────────────────────────┬───────────────────────────────────┘
                              │  本机: GET /healthz, POST /v1/...
                              ▼
┌──────────────────────────────────────────────────────────────┐
│  Python  llm-api (FastAPI, 默认 127.0.0.1:8080)                 │
│  与 go-api 的 proto 使用同一套 Ask 字段                          │
└────────────────────────────┬───────────────────────────────────┘
                              │  DeepSeek 等
                              ▼
                         外部大模型

（可选、完整后端栈）

┌────────────────────────────┬───────────────────────────────────┐
│  客户端/其它服务 (gRPC)        │  go-api 监听 GRPC_ADDR(如 :50051)   │
└────────────────────────────┴───────────────┬───────────────────┘
                                            │  HTTP: PYTHON_AGENT_BASE_URL
                                            ▼
                                    同上 Python llm-api
                    ┌───────────────┴───────────────┐
                    │  MySQL / Redis（go-api 持久化与缓存）  │
                    └───────────────────────────────┘
```

要点：

- **go-api** 对外是 **gRPC**（`MobileArchitectService/AskExpert`），服务内部用 HTTP 去调 **Python**（见 `go-api/.env` 的 `PYTHON_AGENT_BASE_URL`）。
- **本仓库的 Android Demo** 使用 **Retrofit 走 HTTP/JSON**，直接请求 **Python `llm-api`**，与 `llm.http.app` 中路由一致。这样无需在 App 中集成 gRPC-Java，即可复现与 go-api **相同的请求/响应模型**（字段与 `proto/mobile_architect/v1/mobile_architect.proto` 一致）。
- 若你希望 App **直连 gRPC 网关**，需另行引入 `grpc-okhttp` 等，并生成 stub；本文不作展开。

---

## 一、环境先决条件

- **Go 1.22+**（`go version`），并已安装 `protoc` 与 `protoc-gen-go` / `protoc-gen-go-grpc`（`make proto` 会用到，且 `$HOME/go/bin` 在 PATH 中为宜）。
- **MySQL 8+**、**Redis 6+**（与 `go-api/.env.example` 中地址/账号一致，或你自行改 `.env`）。
- **Python 3.9+** 与本仓库已配置的虚拟环境（如项目根 `source .llm/bin/activate`）。
- 根目录 **`.env`**：至少配置 `DEEPSEEK_API_KEY` 等，详见仓库根 `README.md`。

在 MySQL 中创建与 DSN 一致的数据库，例如（名称以 `.env` 为准）：

```sql
CREATE DATABASE IF NOT EXISTS mobile_architect
  DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

---

## 二、启动 Python `llm-api`（Agent HTTP）

在仓库**根目录**：

```bash
source .llm/bin/activate   # 依你本机 venv 路径调整
cp -n .env.example .env    # 若尚未配置
pip install -e . --no-build-isolation
```

使用入口脚本（与 `pyproject.toml` 中 `llm-api` 一致）：

```bash
llm-api
```

或：

```bash
python -m llm.http.server
```

默认监听 **`APP_HTTP_HOST` / `APP_HTTP_PORT`（如 `127.0.0.1:8080`）**。

自测接口：

```bash
curl -sS http://127.0.0.1:8080/healthz
# 期望: {"status":"ok"}
```

---

## 三、启动 go-api（gRPC + MySQL + Redis）

```bash
cd go-api
cp -n .env.example .env
# 按本机情况编辑 .env: GRPC_ADDR, MYSQL_DSN, REDIS_*, PYTHON_AGENT_BASE_URL
make proto
make tidy
make run
```

- **必须先能连上 MySQL 与 Redis**，且 **Python 已按第二节在 `PYTHON_AGENT_BASE_URL` 上 listening**，否则 go-api 启动或首请求时可能失败。
- 服务名：`mobile_architect.v1.MobileArchitectService`，方法：`AskExpert`。

若已安装 [grpcurl](https://github.com/fullstorydev/grpcurl)，在 `go-api` 目录可列举服务（`.proto` 路径按本机调整）：

```bash
grpcurl -proto proto/mobile_architect/v1/mobile_architect.proto \
  -plaintext localhost:50051 list
```

> 将 `50051` 换为你的 `GRPC_ADDR` 端口；若 `GRPC_ADDR` 为 `:50051` 则监听在全部地址。

---

## 四、开发 Android 工程 `LLMClient`

### 4.1 工程位置与依赖

- 路径：仓库根目录下 **`LLMClient/`**。
- 已添加：**Retrofit 2、OkHttp、Logging Interceptor、Kotlinx Coroutines、Lifecycle ViewModel + Compose 集成**。
- 网络层：`com.tcm.llmclient.network.NetworkService` 使用 **协程** `suspend` API（Retrofit 2.6+）。

### 4.2 本机服务地址与模拟器/真机

- **模拟器**访问宿主机本机回环时，应使用 **`10.0.2.2`**，而不是 `127.0.0.1`（`127.0.0.1` 在模拟器内指向模拟器自己）。
- 默认在 `app/build.gradle.kts` 的 **`BuildConfig.LLM_BASE_URL`** 中配置为：  
  **`http://10.0.2.2:8080/`**（指向宿主机 8080 上的 `llm-api`）。
- **真机**请改为与电脑**同一局域网**下电脑的 **局域网 IP**（如 `http://192.168.1.100:8080/`），并在 **`LLMClient/app/src/main/res/xml/network_security_config.xml`** 中为你的 IP **增加** `domain-config`（`cleartextTrafficPermitted="true"` 仅建议开发环境使用，上线请使用 HTTPS + 受信证书策略）。

开发环境已允许对 `10.0.2.2`、`localhost`、`127.0.0.1` 的 HTTP 明文访问，见 `network_security_config.xml`。

### 4.3 Demo 界面行为

- 启动时自动请求 **`GET /healthz`**。
- 可输入问题，点击 **「向 Agent 提问」** 调用 **`POST /v1/mobile-architect/ask`**，展示结构化结果摘要、架构/性能/设计原则、风险与延伸学习点。

### 4.4 构建与运行

```bash
cd LLMClient
./gradlew :app:assembleDebug
# 在 Android Studio 中 Run 到模拟器/真机
```

---

## 五、建议联调顺序（完整栈）

1. 启动 **MySQL**、**Redis**。
2. 配置根目录与 `go-api/.env`。
3. 启动 **Python `llm-api`**（`127.0.0.1:8080`）。
4. 启动 **go-api**（`make run`）— 用 grpcurl 验证 gRPC（可选）。
5. 运行 **LLMClient** 或 curl 打 Python HTTP，确认问答正常。

仅验证 Android 与 Agent 时，**只需第 1 步中数据库不必为 go-api 准备**—可直接启 Python + App；**验证 go-api** 时务必 MySQL/Redis/双服务就绪。

---

## 六、故障排查

| 现象 | 可能原因 |
|------|----------|
| App 中健康检查失败 | `llm-api` 未启动、端口/防火墙、模拟器未用 `10.0.2.2`、真机未改 IP 与网络安全配置。 |
| `llm-api` 400/422 | 请求 JSON 与 `POST /v1/mobile-architect/ask` 字段不对；对照 `llm.http.schemas`。 |
| go-api 无法启动 | MySQL/Redis 不可达、DSN 错误、或 proto 未生成。 |
| go-api 调 Agent 失败 | `PYTHON_AGENT_BASE_URL` 与 Python 实际地址不一致。 |

---

## 七、与仓库其它文档的关系

- Python Agent 与 HTTP 更细的说明见根目录 **`README.md`**。
- go-api 子目录内另有 **`go-api/README.md`** 描述分层与目标。

按本文步骤即可在本地完成 **从 Android 到 Python Agent 的完整 HTTP Demo**；在 **同一条业务链** 上，go-api 以 gRPC 形式承担网关与数据层职责，部署时可按需要把 BFF 与 App 的接入点切到 gRPC 或经反向代理的 HTTP/HTTPS。
