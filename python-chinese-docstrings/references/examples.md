# Python 中文 Docstring 示例

## 模块、类与方法

以下标准库示例展示模块、类与方法的 Docstring，可用于核对文档与实际行为。

```python
"""文本标签读取模块，为命令行和导入入口提供统一的逐行读取规则。"""

from pathlib import Path


class LabelReader:
    """从 UTF-8 文本文件读取标签，跳过空白行并保留原有顺序。

    Attributes:
        source: 存放标签的文本文件路径；创建实例时不会打开文件。
    """

    def __init__(self, source: Path) -> None:
        """保存输入路径，实际文件读取推迟到 read 调用时执行。

        Args:
            source: 每行存放一个标签的文本文件。
        """
        self.source = source

    def read(self) -> list[str]:
        """读取全部非空标签，不去重且不修改源文件。

        Returns:
            已去除首尾空白的标签列表；文件为空或仅有空白行时返回空列表。

        Raises:
            OSError: 文件不存在、不可读或发生其他文件系统错误。
            UnicodeError: 文件内容不能按 UTF-8 解码。
        """
        lines = self.source.read_text(encoding="utf-8").splitlines()
        labels: list[str] = []
        for line in lines:
            label = self._normalize(line)
            if label:
                labels.append(label)
        return labels

    @staticmethod
    def _normalize(line: str) -> str:
        """去除单行文本首尾空白，供 read 统一判断是否包含标签。"""
        return line.strip()
```

## 生成器

```python
from collections.abc import Iterator


def numbered_labels(labels: list[str]) -> Iterator[tuple[int, str]]:
    """按原顺序为标签附上从 1 开始的展示序号。

    Args:
        labels: 已由调用方准备的标签，不在此处去重或修改文本。

    Yields:
        展示序号和对应标签组成的二元组；输入为空时不产生任何结果。
    """
    yield from enumerate(labels, start=1)
```

## 需要据实说明的区别

- async 函数通常仍使用 Returns；包含 yield 的异步生成器使用 Yields。
- 类型提示不能说明超时单位、None 的业务含义或事务归属，这些应写进中文说明。
- 文档写明“不去重”，实现就不能悄悄改成 set；这类不一致应作为审查问题报告。
