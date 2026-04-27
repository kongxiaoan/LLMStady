# RAG Demo

这是项目内置的一个最小可运行 RAG Demo，用来演示：

1. 本地知识库加载
2. 文档切分
3. 检索召回
4. 基于检索上下文让 DeepSeek 生成答案

当前实现故意保持简单，不依赖向量数据库，便于学习。

---

## 命令

```bash
llm-rag-demo "Android 启动优化应该先看哪些指标"
```

也可以指定检索条数：

```bash
llm-rag-demo "Java 六大设计原则怎么落地到 Android 项目" --top-k 2
```

---

## 知识库目录

默认读取：

```text
docs/rag_demo
```

当前内置了三份示例知识文档：

- `android_architecture.md`
- `android_performance.md`
- `java_solid.md`

---

## 工作原理

### 1. 加载文档

从 `docs/rag_demo/*.md` 读取本地知识内容。

### 2. 文档切分

按固定窗口切成多个 chunk。

### 3. 本地检索

使用简单关键词打分，不依赖向量数据库。

### 4. 生成答案

把召回的 chunk 作为上下文，交给 DeepSeek 生成答案。

---

## 为什么这个 Demo 不直接上向量库

因为当前目标是学习 RAG 的最小闭环，而不是直接引入更多基础设施。

这个版本适合先理解：

- 文档为什么要切分
- 检索结果如何进入 Prompt
- 检索和生成是两段不同职责

等这条链路理解清楚后，再升级到：

- embedding
- 向量数据库
- rerank
- 混合检索

---

## 当前局限

这个 demo 有明确局限：

- 中文检索能力比较基础
- 没有 embedding
- 没有向量召回
- 没有 rerank
- 不适合生产环境

它的目标是“易懂”，不是“最强”。

---

## 建议学习顺序

建议按这个顺序读代码：

1. [loader.py](./../src/llm/rag/loader.py)
2. [chunker.py](./../src/llm/rag/chunker.py)
3. [retriever.py](./../src/llm/rag/retriever.py)
4. [service.py](./../src/llm/rag/service.py)
5. [cli.py](./../src/llm/rag/cli.py)
