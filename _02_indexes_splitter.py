#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : Vincent
@Time    : 2026/1/4 17:47
@File    : _02_indexes_splitter.py
@Function :
"""
from langchain_text_splitters import CharacterTextSplitter  # 字符分割
from langchain_text_splitters import RecursiveCharacterTextSplitter  # 递归字符分割
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parents[0] / ".env")

text_splitter = CharacterTextSplitter(
    separator=" ",  # 空格分割，但是空格也属于字符
    chunk_size=5,  # 5个字符为一块
    chunk_overlap=0,  # 0表示不重叠
)

# 一句分割
a = text_splitter.split_text("a b c d e f")
print(a)
# ['a b c', 'd e f']

# 多句话分割（文档分割）
texts = text_splitter.create_documents(["a b c d e f", "e f g h"], )
print(texts)
# [Document(page_content='a b c'), Document(page_content='d e f'), Document(page_content='e f g'), Document(page_content='h')]
text_splitter = CharacterTextSplitter(
    chunk_size=50,
    chunk_overlap=5,
)
recursive_text_splitter = RecursiveCharacterTextSplitter(chunk_size=50, chunk_overlap=5)
text = """2023年以来，随着ChatGPT的火爆，使得LLM成为研究和应用的热点，但是市面上大部分LLM都存在一个共同的问题：
模型都是基于过去的经验数据进行训练完成，无法获取最新的知识，以及各企业私有的知识。因此很多企业为了处理私有的知识，
主要借助一下两种手段来实现

利用企业私有知识，基于开源大模型进行微调
基于LangChain集成向量数据库以及LLM搭建本地知识库的问答（RAG）
RAG（Retrieval-Augmented Generation）检索增强生成，在不改变模型权重的情况下，提升大模型生成能力。
用户query 会从知识库中检索出相关文档，大模型依据文档生成用户的 query 回答。这样可以实现低成本提升大模型的回复能力。
RAG 核心点在于知识库的构建和检索策略。

索引阶段

加载文件
内容提取
文本分割 ，形成chunk
文本向量化
存向量数据库
检索阶段

query向量化
在文本向量中匹配出与问句向量相似的top_k个
生成阶段
匹配出的文本作为上下文和问题一起添加到prompt中
提交给LLM生成答案：
"""
print("RecursiveCharacterTextSplitter", "==" * 50)
for chunk in recursive_text_splitter.create_documents([text]):
    print(f"[{len(chunk.page_content)}]", chunk.page_content)
    print("======" * 10)

print("CharacterTextSplitter", "==" * 50)
for chunk in text_splitter.create_documents([text]):
    print(f"[{len(chunk.page_content)}]", chunk.page_content)
    print("======" * 10)
