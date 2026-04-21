from __future__ import annotations

# 这个边界处理是为了兼容两种启动方式：
# 1. `python -m llm.main`
# 2. `python src/llm/main.py`
# 第二种方式运行时，Python 默认不会把 `src` 自动加入包搜索路径，
# 所以需要在入口文件里做一次轻量修正，避免初学时被导入问题打断。
if __package__ in (None, ""):
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from llm.cli import main


if __name__ == "__main__":
    main()
