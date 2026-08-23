#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : Vincent
@Time    : 2026/4/2 20:54
@File    : model.py
@Function :
qwen模型的封装接口
1. embedding模型。用于文档向量化和query向量化
2. LLM 最终回答
"""
# from langchain_community.chat_models import ChatTongyi
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_openai import ChatOpenAI
import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parents[2] / ".env")

# 创建大模型
llm = ChatOpenAI(
    model="qwen-max",  # 模型名称，在百炼平台的API
    api_key=os.getenv("API_KEY"),  # 百炼平台的API KEY
    base_url=os.getenv("BASE_URL"),  # 百炼平台的base url
)

embeddings = DashScopeEmbeddings(
    model="text-embedding-v1",  # 模型名称，在百炼平台的API
    dashscope_api_key=os.getenv("API_KEY"),  # 百炼平台的API KEY
)

if __name__ == '__main__':
    print(llm.invoke("你好"))
    print(embeddings.embed_query("你好"))
