#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : Vincent
@Time    : 2026/3/24 12:00
@File    : _01_message.py
@Function :
"""
from langchain.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parents[0] / ".env")

llm = ChatOpenAI(
    model="qwen-flash",
    api_key=os.getenv('API_KEY'),
    base_url=os.getenv("BASE_URL"),
)
messages = [
    HumanMessage(content="你好"),
    AIMessage(content="你好，有什么可以帮你？"),
    HumanMessage(content="LangChain 是什么？"),
    AIMessage(content="LangChain 是一个开源的 LLM 应用开发框架，用于构建 LLM 应用。"),
    HumanMessage(content="我问了几个问题了？"),
]

response = llm.invoke(messages)
print(response.content)
