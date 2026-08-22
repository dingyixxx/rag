#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : Vincent
@Time    : 2026/3/24 11:07
@File    : _01_tool_invoke.py
@Function :
"""
from langchain.tools import tool
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parents[0] / ".env")


# 定义工具, 一定要加上工具的docstring，否则无法调用
@tool
def multiply(a: int, b: int) -> int:
    """计算两个数字的乘积"""
    return a * b


@tool
def read_file(file_path: str) -> str:
    """读取文件"""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


if __name__ == '__main__':
    print(multiply.invoke({"a": 3, "b": 4}))
    print(read_file.invoke({"file_path": "_01_tool_invoke.py"}))
