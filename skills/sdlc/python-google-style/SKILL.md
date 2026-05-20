---
name: python-google-style
description: 当用户要求编写 Python 代码、审查 Python 代码、格式化 Python 文件，或项目包含 .py 文件 / pyproject.toml 时触发。强制遵循 Google Python Style Guide 编写 Python 3.10+ 代码。
---

# Python Google Style

## 适用场景
- 编写新的 Python 模块、函数或类
- 审查现有 Python 代码的规范性
- 重构代码以符合团队统一标准

## 强制规范

### 1. 行宽与缩进
- **行宽上限 80 字符**（非 100）。超出时使用隐式换行（括号内），禁止反斜杠 `\` 换行。
- **缩进 4 空格**，禁止 Tab。

```python
# Yes: 括号内隐式换行，与 opening delimiter 对齐
def fetch_rows(
    table_handle: smalltable.Table,
    keys: Sequence[bytes | str],
    require_all_keys: bool = False,
) -> Mapping[bytes, tuple[str, ...]]:
    ...

# No: 反斜杠换行
if width == 0 and height == 0 and \
        color == 'red':
    ...
```

### 2. 导入规则
- 只导入包/模块，禁止 `from x import y` 导入单个类/函数（`typing` 和 `collections.abc` 例外）。
- 禁止相对导入，一律使用完整包路径。
- 分组排序：`__future__` → 标准库 → 第三方 → 本地子包，每组内按完整路径字典序排列。

```python
# Yes
from __future__ import annotations

import collections
import queue
import sys

from absl import app
from absl import flags
import tensorflow as tf

from myproject.backend import huxley
from otherproject.ai import mind

# No
import os, sys                # 同行多导入
from . import utils           # 相对导入
from myproject.backend import * # 通配符导入
```

### 3. 命名规范

| 类型 | 命名 | 示例 |
|:---|:---|:---|
| 模块/包 | snake_case.py | `data_loader.py` |
| 类 | CapWords | `DataLoader` |
| 函数/方法 | snake_case() | `fetch_rows()` |
| 常量 | CAPS_WITH_UNDER | `MAX_RETRY_COUNT` |
| 私有 | 前缀 `_` | `_internal_helper()` |
| 异常 | CapWords + Error | `ConnectionError` |

- 禁止单字符名（循环变量 `i`/`j`/`k` 除外）。
- 禁止在名称中嵌入类型信息（如 `id_to_name_dict`）。
- 禁止模块名含连字符 `-`。

### 4. 类型注解（公共 API 强制）
- 公共函数/方法的参数和返回值必须加类型注解。
- 使用 `X | None`（Python 3.10+）而非 `Optional[X]`，禁止隐式 `a: str = None`。
- 泛型必须带参数：`Sequence[int]` 而非裸 `Sequence`。
- `self`/`cls` 一般不注解；`__init__` 一般不注解返回值。

```python
# Yes
def connect(port: int, timeout: float | None = None) -> Connection:
    ...

def find_users(ids: Sequence[int]) -> Mapping[int, User]:
    ...

# No
def connect(port, timeout=None):        # 无注解
def bad(a: str = None) -> str:          # 隐式 Optional
def get_names(ids: Sequence) -> Mapping: # 裸泛型
```

### 5. 文档字符串（Google 风格）
- 所有公共 API、非平凡函数、类必须有 docstring。
- 使用 `"""` 三引号，首行不超过 80 字符的摘要句。
- 必须包含 `Args:`、`Returns:`（或 `Yields:`）、`Raises:` 段落。

```python
def fetch_smalltable_rows(
    table_handle: smalltable.Table,
    keys: Sequence[bytes | str],
) -> Mapping[bytes, tuple[str, ...]]:
    """Fetches rows from a Smalltable.

    Retrieves rows pertaining to the given keys from the Table instance
    represented by table_handle.

    Args:
        table_handle: An open smalltable.Table instance.
        keys: A sequence of strings representing the key of each table
            row to fetch.

    Returns:
        A dict mapping keys to the corresponding table row data
        fetched. Each row is represented as a tuple of strings.

    Raises:
        IOError: An error occurred accessing the smalltable.
    """
```

### 6. 异常处理
- 禁止裸 `except:`，禁止捕获 `Exception`/`StandardError`（除非重新抛出或隔离点）。
- 禁止用 `assert` 替代前置条件判断，`assert` 可能被优化掉。
- 自定义异常必须以 `Error` 结尾，继承自内置异常类。
- `try` 块内代码最小化。

```python
# Yes
def connect_to_next_port(self, minimum: int) -> int:
    if minimum < 1024:
        raise ValueError(f'Min. port must be at least 1024, not {minimum}.')
    port = self._find_next_open_port(minimum)
    if port is None:
        raise ConnectionError(f'Could not connect on port {minimum} or higher.')
    return port

# No
assert minimum >= 1024, 'Minimum port must be at least 1024.'  # 依赖 assert
try:
    a = fetch()
    b = parse(a)
    c = save(b)
except Exception:          # 太宽泛
    pass
```

### 7. 默认参数值
- 禁止可变对象作为默认值（`list`、`dict`、`set`）。
- 禁止将模块加载时求值的表达式作为默认值（如 `time.time()`、`flags`）。

```python
# Yes
def foo(a: Sequence | None = None) -> None:
    if a is None:
        a = []

# No
def foo(a: list = []):           # 可变默认值
def foo(a: Mapping = {}):        # 可变默认值
def foo(a: float = time.time()): # 模块加载时求值
```

### 8. 字符串与格式化
- 优先使用 f-string、`%` 运算符或 `format` 方法。
- 禁止用 `+` 拼接字符串，循环内禁止 `+=` 累积字符串（用 `list + ''.join()`）。

```python
# Yes
x = f'name: {name}; score: {n}'
items = ['<table>']
for last_name, first_name in employee_list:
    items.append('<tr><td>%s, %s</td></tr>' % (last_name, first_name))
items.append('</table>')
employee_table = ''.join(items)

# No
x = 'name: ' + name + '; score: ' + str(n)
employee_table += '<tr>...</tr>'  # 循环内 +=
```

### 9. 日志与错误消息
- 日志函数（如 `logging.info`）必须使用 `%` 占位符，禁止传 f-string 或裸变量。
- 错误消息必须精确、可 grep、插值部分清晰可辨。

```python
# Yes
logger.info('TensorFlow Version is: %s', tf.__version__)
raise ValueError(f'Not a probability: {p=}')

# No
logger.info(f'TensorFlow Version is: {tf.__version__}')  # f-string 禁止
logger.info(os.getenv('PAGER'))                            # 裸变量禁止
```

### 10. 资源管理
- 必须使用 `with` 语句管理文件、socket、数据库连接等可关闭资源。
- 禁止依赖 `__del__` 做清理。

```python
# Yes
with open("hello.txt") as hello_file:
    for line in hello_file:
        print(line)

# No
f = open("hello.txt")   # 未显式关闭
data = f.read()
```

### 11. 推导式与生成器
- 列表/字典/集合推导式允许，但禁止多层嵌套 `for` 或复杂 filter。
- 生成器函数 docstring 用 `Yields:` 而非 `Returns:`。

```python
# Yes
result = [mapping_expr for value in iterable if filter_expr]

# No
result = [(x, y) for x in range(10) for y in range(5) if x * y > 10]
```

### 12. 条件表达式与 Lambda
- 条件表达式（`x = a if cond else b`）仅用于简单场景，每部分必须单行。
- Lambda 仅限单行（≤60–80 字符），复杂逻辑用嵌套函数。

```python
# Yes
one_line = 'yes' if predicate(value) else 'no'

# No
portion_too_long = ('yes'
                    if some_long_module.some_long_predicate_function(
                        really_long_variable_name)
                    else 'no, false, negative, nay')
```

### 13. True/False 评估
- 优先使用隐式 false：`if users:` 而非 `if len(users) == 0:`。
- 必须显式用 `is None` / `is not None` 判断 `None`。
- 布尔变量禁止与 `False` 用 `==` 比较。

```python
# Yes
if not users:
    print('no users')
if timeout is None:
    timeout = DEFAULT_TIMEOUT
if not x and x is not None:
    ...

# No
if len(users) == 0:
    print('no users')
if x == False:
    ...
```

### 14. 可变全局状态
- 禁止可变全局状态。模块级常量允许（`ALL_CAPS`）。
- 如确需全局状态，前缀 `_` 并通过公共函数访问。

```python
# Yes
_MAX_HOLY_HANDGRENADE_COUNT = 3  # 常量允许

# No
_active_connections = []  # 可变全局状态
```

### 15. 函数长度与 Main 入口
- 无硬性行数限制，但超过 40 行应考虑拆分。
- 可执行文件必须有 `main()` 函数，并用 `if __name__ == '__main__':` 保护。

```python
def main(argv: Sequence[str]) -> None:
    ...

if __name__ == '__main__':
    app.run(main)
```

## 速查：Google Style Docstring 模板

```python
def function_name(param1: type, param2: type | None = None) -> ReturnType:
    """One-line summary ending with period.

    Longer description if needed.

    Args:
        param1: Description of param1.
        param2: Description of param2. Defaults to None.

    Returns:
        Description of return value.

    Raises:
        ValueError: If param1 is invalid.
        IOError: If file access fails.
    """
```

## 一致性原则（BE CONSISTENT）

如果你正在编辑已有文件，花几分钟观察周围代码的风格。如果现有代码使用 `_idx` 后缀命名索引变量，你也应该这样做。风格指南的目的是建立共同词汇，让人们专注于"说什么"而非"怎么说"。

## Gotchas

- **行宽是硬限制 80**：不是 88（Black 默认），也不是 100。超出时必须用括号隐式换行，绝不用反斜杠。
- **typing 例外**：`from typing import Optional` 等类型导入是允许的，但生产代码中优先用 `X | None`（Python 3.10+）。
- **logging 占位符**：`logger.info('msg: %s', value)` 是强制的，传 f-string 会导致日志框架延迟格式化失效，影响性能且无法安全处理非字符串类型。
- **assert 不是校验工具**：`assert` 在 `python -O` 下会被优化掉，永远不要用 assert 做用户输入校验或业务前置条件检查。
- **相对导入的坑**：Google Style 禁止相对导入，因为在复杂包结构和不同入口点执行时，相对导入极易出现 `ImportError` 或重复导入。
- **不要在名称里嵌入类型**：如 `id_to_name_dict`、`username_list`。如果类型变了，名称也要跟着改，维护成本极高。
- **f-string 与 logging**：f-string 本身没问题，但 logging 函数的参数里禁止用，其他地方鼓励用。
- **修改已有文件时优先保持一致**：即使旧代码不完全符合本规范，也不要在同一次 PR 中混合风格，除非是专门的重构提交。
