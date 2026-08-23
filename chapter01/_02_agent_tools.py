#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : Vincent
@Time    : 2026/1/4 16:49
@File    : _09_agent_tools.py
@Function :
"""
from langchain.tools import tool
from langchain_openai import ChatOpenAI
import os
from langchain.agents import create_agent
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parents[0] / ".env")


@tool
def write_file(file_path: str, content: str) -> str:
    """
    把content写入文件路径file_path
    """
    with open(file_path, "w", encoding="utf-8") as writer:
        writer.write(content)

    print(f"写入文件{file_path} 成功")


@tool
def multiply(a: int, b: int) -> int:
    """用于计算两个整数的乘积。"""
    print(f"正在执行乘法: {a} * {b}")
    return a * b


@tool
def add(a: int, b: int) -> int:
    """用于计算两个整数的乘积。"""
    print(f"正在执行加法: {a} * {b}")
    return a + b


llm = ChatOpenAI(
    model="qwen-flash",
    api_key=os.getenv('API_KEY'),
    base_url=os.getenv("BASE_URL"),
)

tools = [write_file, add, multiply]

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt="你是系统助手，需要根据用户的输入决定是否调用工具完成任务"
)

print(agent.invoke({"messages": "计算100加888的结果？"}))
print(agent.invoke({"messages": "解释下什么是注意力机制，写入当前目录下，文件名称自己起一个，编码要是utf-8的"}))
print(agent.invoke({"messages": "我已经问了几个问题？"}))  # 没有手动实现message功能
messages = [{"role": "user", "content": "计算100加21的结果？"}]
messages = agent.invoke({"messages": messages})
for each in messages["messages"]:
    print(each)
