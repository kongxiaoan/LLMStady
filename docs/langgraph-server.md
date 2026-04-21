# LangGraph Server 是什么

这份文档结合当前项目来解释：

1. `LangGraph Server` 是什么
2. 它和 `LangChain`、`LangGraph`、`LangSmith` 的关系
3. 你当前项目有没有在用它
4. 什么时候应该引入它
5. 如果后续 API 层想用 Go + gRPC，LangGraph Server 该放在什么位置

---

## 一句话理解

`LangGraph Server` 可以理解成：

> 把你的 Agent / Graph 以服务形式运行起来的官方运行服务器。

它不是“让你写 Agent 逻辑”的那层，而是“让你部署、运行、管理 Agent”的那层。

---

## 它和几个常见名词的关系

很多人在 LangChain 生态里容易把几个名字混在一起。

### 1. LangChain

LangChain 更像是高层开发框架。

你现在项目里这句：

```python
from langchain.agents import create_agent
```

就是 LangChain 的高层 API。

它适合：

- 快速搭 Agent
- 组合模型和工具
- 做结构化输出
- 管理 Prompt、Middleware、Context

---

### 2. LangGraph

LangGraph 是底层 Agent / Workflow runtime。

官方文档明确说明：

> LangChain 的 `create_agent` 底层跑在 LangGraph 之上。

也就是说，你虽然没直接写 `StateGraph`，但已经在间接使用 LangGraph 的运行时能力。

比如你当前项目里 [factory.py](/Users/Zhuanz/android/llm/src/llm/agent/factory.py:1) 这段：

```python
return create_agent(
    model=model,
    tools=MOBILE_EXPERT_TOOLS,
    system_prompt=SYSTEM_PROMPT,
    response_format=ExpertAnswer,
    context_schema=RuntimeContext,
    checkpointer=build_checkpointer(),
    debug=settings.debug,
    name="mobile-architect-agent",
)
```

这里的：

- `context_schema`
- `checkpointer`
- `invoke`

这些能力背后都和 LangGraph runtime 有关系。

---

### 3. LangGraph Server

LangGraph Server 是把 Agent / Graph 运行成服务的一层。

它通常提供这些能力：

- HTTP API
- assistants / threads / runs 管理
- 持久化
- streaming
- checkpoint
- human-in-the-loop
- time travel
- webhook
- MCP / A2A 等服务能力

它的角色不是“开发框架”，而是“运行与服务托管层”。

---

### 4. LangSmith

LangSmith 是观测、调试、评估平台。

它负责：

- trace
- 调试
- 评估
- 监控

它不是用来写 Agent 的，也不是用来跑服务的。

---

## 当前项目现在处于哪一层

你现在项目的状态是：

- 用 `LangChain` 写 Agent
- 底层运行在 `LangGraph runtime`
- 还没有真正使用 `LangGraph Server`
- 也还没有把 Agent 部署成独立服务

也就是说，你现在是：

> 本地 Python 进程直接运行 Agent

而不是：

> 一个独立 Agent Server 对外暴露 API

---

## 为什么很多人感觉“我没用 LangGraph”

因为你现在没有显式写这种代码：

```python
from langgraph.graph import StateGraph
```

也没有自己去建：

- 节点
- 边
- 状态图

所以直觉上会觉得“我没用 LangGraph”。

但从运行时角度说，你已经在用了，因为：

- `create_agent` 底层就是基于 LangGraph runtime

你现在没显式使用的是：

- LangGraph Graph API
- LangGraph Server

---

## LangGraph Server 解决什么问题

当项目从“本地脚本”走向“可被别的系统调用的服务”时，就会遇到一类新问题：

- 如何管理多轮会话
- 如何管理线程和 run
- 如何保存执行状态
- 如何中断后恢复
- 如何做 streaming
- 如何把 Agent 暴露成稳定服务
- 如何支持生产化部署

这些问题不是 `create_agent` 一句能解决的。

LangGraph Server 就是为这些问题服务的。

---

## 什么时候适合引入 LangGraph Server

### 场景 1：要对外提供服务

比如：

- Web 前端调 Agent
- App 调 Agent
- 内部平台调 Agent
- 其他服务调 Agent

这时候 Agent 不再是“一个本地函数”，而是一个“后端服务能力”。

---

### 场景 2：需要多轮线程管理

你现在虽然已经有：

```python
thread_id
```

但还是在本地代码里手动传。

如果以后要支持真实用户、多设备、长期会话，就需要：

- thread 管理
- run 管理
- 状态持久化

LangGraph Server 会更自然。

---

### 场景 3：要做更强的可观测与运维

比如：

- 流式返回
- 失败恢复
- 断点继续
- 人工审批节点
- time travel

这些能力在 Agent Server 场景下价值更大。

---

## 当前项目未来可以怎么演进

你现在的项目是一个很好的“本地学习版”。

未来可以按这个顺序升级：

### 第一步：继续保持本地版

先把这些理解透：

- `create_agent`
- `context_schema`
- `response_format`
- tools
- checkpoint

---

### 第二步：改造成显式 LangGraph Graph

比如把“移动端专家 Agent”拆成几个节点：

- 问题分类节点
- 架构分析节点
- 性能分析节点
- 原则映射节点
- 总结输出节点

这一步是从“高层 Agent API”进入“显式编排”。

---

### 第三步：部署为 LangGraph Server

这时你的 Agent 不再只是本地 CLI，而是正式服务。

---

## 如果 API 层希望用 Go + gRPC，应该怎么理解 LangGraph Server 的位置

这是一个很好的方向，而且很工程化。

建议你把整体架构拆成两层：

### 方案 A：Python Agent 服务层 + Go API 网关层

推荐理解如下：

1. Python 层
   负责：
   - LangChain / LangGraph Agent 逻辑
   - Prompt
   - Tool
   - 模型调用
   - 状态与记忆

2. Go 层
   负责：
   - gRPC API
   - 鉴权
   - 限流
   - 超时控制
   - 请求编排
   - 统一日志 / 监控
   - 对客户端暴露稳定契约

在这个架构里，LangGraph Server 所在位置是：

> Python Agent 服务层的一部分

而 Go gRPC 服务是它的上层 API 网关。

也就是：

```text
Client / App
    ->
Go gRPC API
    ->
Python Agent Service (LangChain / LangGraph / LangGraph Server)
    ->
DeepSeek / Tools / Memory / Store
```

---

## 为什么不建议一开始就让 Go 直接承载 Agent 逻辑

因为你当前技术栈目标非常明确：

- 用 LangChain 学 Agent
- 用 Python 跑 Agent 生态
- 用 DeepSeek 做模型层

这时如果把 Agent 逻辑也强行迁到 Go，会有几个问题：

1. 生态不如 Python 成熟
2. 学习成本会被双倍拉高
3. 官方最新样例和文档主要集中在 Python
4. 你本来想学的是 Agent，不是先解决跨语言生态问题

所以更专业的做法通常不是：

> 用 Go 重写 Agent

而是：

> 用 Go 作为 API 层，用 Python 作为 Agent 运行层

这正好符合典型的多语言分层设计。

---

## 推荐的职责边界

### Python Agent 层负责

- 提示词工程
- Tool 编排
- 模型调用
- Agent 状态
- checkpoint
- 长期记忆
- LangSmith trace

### Go gRPC 层负责

- Protobuf 契约
- gRPC 服务暴露
- 统一鉴权
- 配额控制
- 请求幂等
- 灰度发布
- 统一监控埋点
- 上下游服务集成

这样的边界非常清晰，也更符合生产系统设计。

---

## 你的项目下一阶段可以怎么做

如果你要朝 “Go gRPC API + Python Agent” 演进，我建议分三步：

1. 先把当前 Python Agent 项目稳定下来
2. 给 Python Agent 增加一个服务入口
   可以是：
   - FastAPI
   - 直接 LangGraph Server
3. 再在 Go 中加 gRPC API 层，作为统一对外入口

这样路线最稳。

---

## 对当前项目的建议结论

对你现在这个学习项目，我建议是：

- 继续用 Python 写 Agent 本体
- 把 LangGraph Server 作为“下一阶段部署层”理解
- 后面如果要接业务系统，再由 Go 实现 gRPC API 层

这是一个很专业、也很符合真实工程分层的方向。

---

## 参考资料

- LangGraph v1：<https://docs.langchain.com/oss/python/releases/langgraph-v1>
- LangChain Runtime：<https://docs.langchain.com/oss/python/langchain/runtime>
- Agent Server：<https://docs.langchain.com/langgraph-platform/langgraph-server>
- LangGraph CLI：<https://docs.langchain.com/langgraph-platform/cli>
- Studio Quickstart：<https://docs.langchain.com/langgraph-platform/quick-start-studio>
