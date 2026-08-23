#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : Vincent
@Time    : 2026/4/2 21:01
@File    : db.py
@Function :
  - 加载文件
  - 内容提取
  - 文本分割 ，形成chunk
  - 文本向量化
  - 存向量数据库
"""
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma  # Chroma 轻量级向量数据库 本地文件
import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parents[2] / ".env")

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
os.chdir(Path(__file__).resolve().parent)

from model import embeddings


def create_db(file_path, embeddings, persist_directory='./chroma'):
    """
    创建向量数据库
    :param file_path: 文档路径
    :param embeddings:  embeddings对象
    :param persist_directory: 持久化目录
    :return:
    """
    if os.path.exists(persist_directory):
        retriever = Chroma(persist_directory=persist_directory,
                           embedding_function=embeddings).as_retriever(
            search_kwargs={'k': 2})
        return retriever
    # 第1步：加载文档
    loader = PyMuPDFLoader(file_path)
    docs = loader.load()  # 列表 List[Document]

    # 第二步：内容提取和分割
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=50,  # 块的大小
        chunk_overlap=15  # 重叠，避免切掉知识库
    )
    split_texts = text_splitter.split_documents(docs)
    # print(split_texts)

    # 第三步：将 document 通过 embeddings 对象计算得到向量信息并永久存入 Chroma 向量数据库，用于后续匹配查询
    vector_db = Chroma.from_documents(
        documents=split_texts,  # 分割以后的文档
        embedding=embeddings,  # embeddings 对象
        persist_directory=persist_directory  # 持久化目录
    )

    # 第四步 返回检索器
    retriever = vector_db.as_retriever(search_kwargs={'k': 2})
    return retriever


if __name__ == '__main__':

    retriever = create_db('./data/物流信息.pdf', embeddings)
    print("======" * 10)
    query = "我的订单什么时候到"
    for doc in retriever.invoke(query):
        print("=====")
        print(doc.page_content)
