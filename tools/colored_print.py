"""
彩色终端打印工具，支持 RED / YELLOW / BLUE。
使用 ANSI 转义码，在支持颜色的终端中生效。
"""

from typing import Any

# ANSI 颜色码（前景色）
LOG_RED = "\033[31m"
LOG_YELLOW = "\033[33m"
LOG_BLUE = "\033[34m"
RESET = "\033[0m"


class ColoredPrint:
    """支持 LOG_RED、LOG_YELLOW、LOG_BLUE 的打印类。"""

    RED = LOG_RED
    YELLOW = LOG_YELLOW
    BLUE = LOG_BLUE
    RESET = RESET

    @classmethod
    def print(cls, *args: Any, color: str = "", **kwargs: Any) -> None:
        """带颜色前缀打印，结尾恢复默认色。"""
        sep = kwargs.pop("sep", " ")
        text = sep.join(str(a) for a in args)
        out = (color + text + cls.RESET) if color else text
        print(out, **kwargs)

    @classmethod
    def red(cls, *args: Any, **kwargs: Any) -> None:
        """红色打印。"""
        cls.print(*args, color=cls.RED, **kwargs)

    @classmethod
    def yellow(cls, *args: Any, **kwargs: Any) -> None:
        """黄色打印。"""
        cls.print(*args, color=cls.YELLOW, **kwargs)

    @classmethod
    def blue(cls, *args: Any, **kwargs: Any) -> None:
        """蓝色打印。"""
        cls.print(*args, color=cls.BLUE, **kwargs)
