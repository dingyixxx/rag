#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : Vincent
@Time    : 2026/4/2 21:13
@File    : main.py
@Function :
检索的主流程
  - query向量化
  - 在文本向量中匹配出与问句向量相似的top_k个
  - 匹配出的文本作为上下文和问题一起添加到prompt中
  - 提交给LLM生成答案：
"""
import os
import sys
from pathlib import Path
# 自举：保证通过 profiler 等包装器运行时，同目录模块可导入、相对路径有效
sys.path.insert(0, str(Path(__file__).resolve().parent))
os.chdir(Path(__file__).resolve().parent)

from model import llm, embeddings
from db import create_db
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parents[2] / ".env")

# 创建向量数据库，获取检索器
retriever = create_db('./data/物流信息.pdf', embeddings)


def generate_prompt(query):
    """
    生成prompt
    :param query: 用户的问题
    :return: 完整的提示词
    """
    # query向量化
    # 在文本向量中匹配出与问句向量相似的top_k个
    context_list = retriever.invoke(query)  # 返回的是topK的文档
    contexts = "\n\n".join([doc.page_content for doc in context_list])

    prompt = f"""
    你是一个智能助手，根据下面的内容回答用户的问题，你不能随便回答，只能依据下面的内容回答。
    检索出的内容如下：
    {contexts}
    
    用户的问题是：{query}
    请回答用户的问题：
    """
    # print(prompt)
    return prompt


def qa(question):
    """
    question：用户的问题
    """
    prompt = generate_prompt(question)
    return llm.invoke(prompt).content


if __name__ == '__main__':
    print(qa("我用的是什么快递"))
