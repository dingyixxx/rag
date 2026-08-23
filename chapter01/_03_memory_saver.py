#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : Vincent
@Time    : 2026/3/22 18:38
@File    : _03_memory_saver.py
@Function :
"""
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain_openai import ChatOpenAI
import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parents[0] / ".env")

llm = ChatOpenAI(
    model="qwen-max",
    api_key=os.getenv('API_KEY'),
    base_url=os.getenv("BASE_URL"),
)

agent = create_agent(
    model=llm,
    checkpointer=InMemorySaver(),
)
print(agent)
config = {"configurable": {"thread_id": "1"}}
print(agent.invoke(
    {"messages": [{"role": "user", "content": "你能做什么"}]},
    config=config,
))
print(agent.invoke(
    {"messages": [{"role": "user", "content": "小明有3个苹果和4个李子，他一共有几个水果"}]},
    config,
))
result = agent.invoke(
    {"messages": [{"role": "user", "content": "我问了几个问题了"}]},
    {"configurable": {"thread_id": "1"}},
)
print(result['messages'][-1].content)
