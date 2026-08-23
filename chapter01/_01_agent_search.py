#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : Vincent
@Time    : 2026/1/4 16:44
@File    : _08_agent.py
@Function :
pip install -U ddgs
pip install numexpr
查询中国人口，接入搜索引擎
"""
import re
import requests
# pip install duckduckgo-search
from langchain_core.tools import tool
import os
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
# from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_community.tools import DuckDuckGoSearchRun
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parents[1] / ".env")


ddg_search = DuckDuckGoSearchRun()
# 实例化大模型
llm = ChatOpenAI(
    model="qwen-max",
    api_key=os.getenv('API_KEY'),
    base_url=os.getenv("BASE_URL"),
)

agent = create_agent(
    model=llm,
    tools=[ddg_search],
    system_prompt="""你是一个有用的个人助手，根据用户的输入内容选择对应的工具，解答用户的问题"""
)


print('agent', agent)

# 代理Agent工作
# response = agent.invoke(
#     {"messages": [
#         {"role": "user", "content": "2025年上海有多少量小汽车"}
#     ]}
# )
# for msg in response["messages"]:
#     print(msg)

for chunk in agent.stream(
        {"messages": [
            {"role": "user", "content": "赵薇的真心不假这首歌,在哪里可以听到"}
        ]}
):
    print(chunk)
