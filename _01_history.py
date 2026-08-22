#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : Vincent
@Time    : 2026/3/24 12:02
@File    : _02_history.py
@Function :
"""
from langchain_community.chat_message_histories import ChatMessageHistory
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

history = ChatMessageHistory()
history.add_user_message("你能做什么")  # 添加用户消息
history.add_ai_message("你好，我能做的事情很多")  # 添加AI消息
history.add_user_message("小明有3个苹果和4个李子，他一共有几个水果")
history.add_ai_message("小明一共有7个水果")
history.add_user_message("我一共问了几个问题了")
print(history.messages)

print(llm.invoke(history.messages))
# content='到目前为止，您一共问了3个问题。第一个问题是关于我能做什么，第二个问题是关于小明有多少个水果，第三个就是当前这个问题，询问您一共问了多少个问题。'
