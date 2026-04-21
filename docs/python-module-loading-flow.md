# Python 模块真实加载顺序说明

这份文档基于当前项目的真实代码，串一次下面这条命令的加载过程：

```bash
python src/llm/main.py
```

同时也会说明它和下面这条命令的差别：

```bash
python -m llm.main
```

---

## 先说结论

Python 不是“等你调用某个函数时，才去加载对应文件”。

更准确地说：

1. Python 会先加载入口文件。
2. 入口文件中的**顶层代码**会按从上到下顺序执行。
3. 遇到 `import` / `from ... import ...` 时，会先去加载被导入模块。
4. 被导入模块也会执行自己的顶层代码。
5. 所有导入完成后，再回到入口文件继续向下执行。
6. 只有真正调用函数时，函数体里的代码才会执行。

---

## 什么叫顶层代码

顶层代码，指的是“不在函数体、不在类方法体里的代码”。

比如下面这些都属于顶层代码：

```python
from llm.cli import main

VALUE = 123

def hello():
    print("hello")

if __name__ == "__main__":
    main()
```

说明：

- `from llm.cli import main` 是顶层代码
- `VALUE = 123` 是顶层代码
- `def hello(): ...` 这一行定义函数本身也是顶层代码
- 但 `print("hello")` 不会在模块加载时执行，因为它在函数体里

---

## 当前项目的真实入口

当前项目入口文件是 [src/llm/main.py](/Users/Zhuanz/android/llm/src/llm/main.py:1)：

```python
from __future__ import annotations

if __package__ in (None, ""):
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from llm.cli import main


if __name__ == "__main__":
    main()
```

---

## 一、执行 `python src/llm/main.py` 时发生了什么

### 第 1 步：Python 把 `src/llm/main.py` 当成脚本入口

这时当前模块名会被设成：

```python
__name__ == "__main__"
```

而且此时通常：

```python
__package__ in (None, "")
```

这就是为什么你在当前项目里看到有这段“边界兼容代码”：

```python
if __package__ in (None, ""):
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
```

它的作用是把 `src` 目录加入 `sys.path`，这样 Python 才能正确找到 `llm` 包。

如果没有这段代码，下面这句通常会失败：

```python
from llm.cli import main
```

因为直接运行文件时，Python 不一定自动把 `src` 当成包搜索根目录。

---

### 第 2 步：执行 `from llm.cli import main`

这时 Python 会暂停继续执行 `main.py`，转去加载 [src/llm/cli.py](/Users/Zhuanz/android/llm/src/llm/cli.py:1)。

也就是说，流程会从：

- `main.py`

跳到：

- `cli.py`

---

## 二、加载 `cli.py` 时发生了什么

`cli.py` 顶部代码如下：

```python
from __future__ import annotations

import argparse
from dataclasses import asdict

from llm.agent.runner import MobileArchitectAssistant
from llm.domain.models import RuntimeContext
```

Python 会按顺序执行这些顶层代码。

说明：

1. `from __future__ import annotations`
   先执行。
2. `import argparse`
   导入标准库。
3. `from dataclasses import asdict`
   导入标准库。
4. `from llm.agent.runner import MobileArchitectAssistant`
   这里会继续跳去加载 `runner.py`。
5. `from llm.domain.models import RuntimeContext`
   要等上一步完成后再继续。

也就是说，`cli.py` 还没加载完，就已经会继续深入到 `runner.py`。

---

## 三、加载 `runner.py` 时发生了什么

[src/llm/agent/runner.py](/Users/Zhuanz/android/llm/src/llm/agent/runner.py:1) 顶部是：

```python
from __future__ import annotations

from dataclasses import dataclass

from llm.agent.factory import build_mobile_architect_agent
from llm.config import Settings, load_settings
from llm.domain.models import ExpertAnswer, RuntimeContext
```

这一步里，Python 会继续递归加载：

- `llm.agent.factory`
- `llm.config`
- `llm.domain.models`

这里要注意一个点：

虽然 `runner.py` 里定义了 `MobileArchitectAssistant` 类，但只有“类定义本身”会在模块加载阶段执行；
类里的方法体，例如 `ask()`，不会现在运行。

---

## 四、加载 `factory.py` 时发生了什么

[src/llm/agent/factory.py](/Users/Zhuanz/android/llm/src/llm/agent/factory.py:1) 顶部代码：

```python
from __future__ import annotations

from langchain.agents import create_agent
from langchain_deepseek import ChatDeepSeek
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer

from llm.config import Settings
from llm.domain.models import ExpertAnswer, RuntimeContext
from llm.prompts.system_prompt import SYSTEM_PROMPT
from llm.tools import MOBILE_EXPERT_TOOLS
```

这一步会继续加载：

- 第三方库 `langchain`、`langchain_deepseek`、`langgraph`
- 项目内模块 `config.py`
- 项目内模块 `domain/models.py`
- 项目内模块 `prompts/system_prompt.py`
- 项目内模块 `tools/__init__.py`

注意：

这里虽然定义了：

- `build_chat_model`
- `build_checkpointer`
- `build_mobile_architect_agent`

但这些函数体此时仍然不会执行。

只是“函数对象被创建好了”。

---

## 五、加载 `config.py` 时发生了什么

[src/llm/config.py](/Users/Zhuanz/android/llm/src/llm/config.py:1) 顶部会执行：

- 常量定义
- `Settings` 类定义
- `_read_bool` / `_read_int` / `_read_float` 函数定义
- `load_settings` 函数定义

但是：

```python
settings = load_settings()
```

这种语句当前文件里并不存在，所以**加载 `config.py` 时不会真的读取 `.env`**。

这是一个很重要的理解点：

- 定义 `load_settings()` 不等于执行 `load_settings()`
- 只有后面真正调用它时，配置才会被读取

---

## 六、加载 `domain/models.py` 时发生了什么

[src/llm/domain/models.py](/Users/Zhuanz/android/llm/src/llm/domain/models.py:1) 会定义两个 dataclass：

- `RuntimeContext`
- `ExpertAnswer`

这里也只是定义类型，不会创建实例。

---

## 七、加载 `tools/__init__.py` 时发生了什么

[src/llm/tools/__init__.py](/Users/Zhuanz/android/llm/src/llm/tools/__init__.py:1) 的内容是：

```python
from llm.tools.architecture import architecture_advisor
from llm.tools.performance import performance_diagnoser
from llm.tools.principles import solid_principles_advisor
from llm.tools.profile import runtime_profile_reader
from llm.tools.review import code_review_checklist_builder

MOBILE_EXPERT_TOOLS = [
    runtime_profile_reader,
    architecture_advisor,
    performance_diagnoser,
    solid_principles_advisor,
    code_review_checklist_builder,
]
```

所以这里会继续加载 5 个工具模块：

- `architecture.py`
- `performance.py`
- `principles.py`
- `profile.py`
- `review.py`

每个工具模块在加载时会：

- 导入 `langchain.tools.tool`
- 定义普通函数
- 再通过 `@tool` 把它包装成 LangChain Tool

这一步是会发生的，因为装饰器本身在定义阶段就会执行。

所以要记住：

- 普通函数体不会现在运行
- 但 `@tool` 这种装饰器会在函数定义时参与执行

---

## 八、依赖模块都加载完成后，开始回退

当 `factory.py`、`config.py`、`models.py`、`tools` 等模块都加载完成后，
Python 会一层层返回：

1. 返回到 `runner.py`
2. `runner.py` 完成 `MobileArchitectAssistant` 类定义
3. 返回到 `cli.py`
4. `cli.py` 完成函数定义：
   - `build_parser`
   - `_build_context`
   - `_print_response`
   - `main`
5. 返回到 `main.py`

此时：

```python
from llm.cli import main
```

终于完成。

---

## 九、回到 `main.py` 最后一段

这时继续执行：

```python
if __name__ == "__main__":
    main()
```

因为当前是直接脚本运行，所以：

```python
__name__ == "__main__"
```

条件成立，于是开始真正调用：

```python
llm.cli.main()
```

注意，到这里才开始进入“业务逻辑执行阶段”。

---

## 十、真正进入 `cli.main()` 后的执行顺序

在 [src/llm/cli.py](/Users/Zhuanz/android/llm/src/llm/cli.py:1) 中，`main()` 的顺序是：

1. `build_parser()`
   构造命令行参数解析器。
2. `parser.parse_args()`
   解析用户输入。
3. 读取 `question`
4. 创建 `MobileArchitectAssistant()`
5. 调用 `assistant.ask(...)`
6. 调用 `_print_response(...)`

---

## 十一、`MobileArchitectAssistant()` 创建时发生了什么

当执行：

```python
assistant = MobileArchitectAssistant()
```

会进入 [runner.py](/Users/Zhuanz/android/llm/src/llm/agent/runner.py:1) 里的 dataclass 初始化流程。

因为它定义了：

```python
def __post_init__(self) -> None:
    self.settings = self.settings or load_settings()
    self.agent = build_mobile_architect_agent(self.settings)
```

所以这里会真正执行：

1. `load_settings()`
   这时才真正读取 `.env`
2. `build_mobile_architect_agent(settings)`
   这时才真正创建 DeepSeek 模型、checkpointer、LangChain Agent

这说明一件很重要的事：

**配置读取和 Agent 创建不是在模块加载时发生的，而是在对象实例化时发生的。**

这种写法更专业，因为它避免了“导入模块就产生副作用”。

---

## 十二、`assistant.ask()` 时发生了什么

执行：

```python
response = assistant.ask(...)
```

会进入：

```python
self.agent.invoke(...)
```

这时候才是真正的 LLM 调用阶段。

LangChain 会在这里：

1. 把用户问题包装成消息
2. 把 `RuntimeContext` 作为上下文传给 Agent
3. 根据系统提示词和工具定义决定是否调用工具
4. 调用 DeepSeek 模型
5. 把结果约束成 `ExpertAnswer`

最后返回结构化结果给 CLI。

---

## 十三、为什么说 Python 不是“按调用顺序加载”

很多初学者容易以为：

> 我调用了 `main()`，所以 Python 才去加载 `cli.py`、`runner.py`、`factory.py`

这不完全对。

更真实的顺序是：

1. 先加载入口模块
2. 入口模块遇到 import
3. 先加载依赖模块
4. 依赖模块全部准备好
5. 最后才调用 `main()`

所以“模块加载”发生在“函数真正调用之前”。

---

## 十四、`python -m llm.main` 有什么不同

如果执行的是：

```bash
python -m llm.main
```

差别主要在入口阶段。

这时 Python 会把它当“包模块”运行，而不是“裸文件脚本”运行。

因此：

- `__name__` 仍然会是 `__main__`
- 但 `__package__` 会是 `llm`

所以这段代码不会执行：

```python
if __package__ in (None, ""):
    ...
```

因为包路径已经由 Python 正确处理好了，不需要手动改 `sys.path`。

除此之外，后面的导入链和运行顺序基本一致。

---

## 十五、一张简化版真实流程图

### 执行 `python src/llm/main.py`

1. 加载 `main.py`
2. 检查 `__package__`
3. 手动把 `src` 加入 `sys.path`
4. 导入 `llm.cli`
5. `cli.py` 导入 `llm.agent.runner`
6. `runner.py` 导入 `llm.agent.factory`
7. `factory.py` 导入：
   `llm.config`
   `llm.domain.models`
   `llm.prompts.system_prompt`
   `llm.tools`
8. `llm.tools` 再导入各个 tool 模块
9. 所有模块加载完成，返回到 `main.py`
10. 执行 `main()`
11. `cli.main()` 解析参数
12. 创建 `MobileArchitectAssistant()`
13. `__post_init__()` 中读取配置并创建 Agent
14. `assistant.ask()` 调用 DeepSeek
15. 打印结构化结果

---

## 十六、学习这个顺序时最该抓住的 4 个点

1. 顶层代码在模块加载时执行。
2. 函数体不会因为“定义了函数”就执行。
3. `import` 会打断当前文件，优先递归加载依赖模块。
4. 真正的业务逻辑通常应放在函数、类方法、或 `if __name__ == "__main__":` 之后，避免导入即副作用。

---

## 十七、为什么当前项目这样设计

这个项目把“副作用”尽量后置了：

- `config.py` 只定义配置，不在导入时直接读 `.env`
- `factory.py` 只定义构造函数，不在导入时直接创建模型
- `runner.py` 直到实例化 `MobileArchitectAssistant` 时才真正加载配置并创建 Agent
- `cli.py` 直到执行 `main()` 时才真正处理用户输入

这种写法在真实工程里很重要，因为它带来三个好处：

1. 可测试
2. 可维护
3. 导入模块时更安全，不容易产生隐藏副作用

---

## 十八、一句话总结

对当前项目来说，你可以把真实执行顺序记成这句话：

> 先按顶层代码递归加载模块，再回到入口执行 `main()`，最后在 `main()` 内部逐步触发配置读取、Agent 创建和模型调用。
