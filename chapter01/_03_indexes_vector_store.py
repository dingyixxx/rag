#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : Vincent
@Time    : 2026/1/4 17:47
@File    : _03_indexes_vector_store.py
@Function :
"""
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parents[0] / ".env")

# 1. 读取文档
with open('data/shufe.txt', encoding='utf-8') as f:
    state_of_the_union = f.read()
# 文档分割
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=10,
    separators=["\n\n", "\n", "。", " ", ""]
)
texts = text_splitter.split_text(state_of_the_union)
# print(texts)

# 3. 向量化，创建embedding模型
embeddings = DashScopeEmbeddings(
    model="text-embedding-v1",  # text-embedding-v3
    dashscope_api_key=os.getenv('API_KEY')
)

# 4. 创建向量数据库
docsearch = Chroma.from_texts(texts, embeddings, persist_directory="outputs/chroma.db")

# 5. 测试检索
query = "学生们称称谁为馆长？"
# docs = docsearch.similarity_search(query, k=2)
# print("长度为", len(docs), docs)


# 创建检索器
retriever = docsearch.as_retriever(search_kwargs={"k": 2})
print("长度为", len(retriever.invoke(query)), retriever.invoke(query))
