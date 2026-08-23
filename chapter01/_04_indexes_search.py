#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : Vincent
@Time    : 2026/1/4 18:11
@File    : _16_indexes_search.py
@Function :
"""
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import DashScopeEmbeddings
import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parents[0] / ".env")

loader = TextLoader('data/shufe.txt', encoding='utf-8')
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=0)
texts = text_splitter.split_documents(documents)

embeddings = DashScopeEmbeddings(
    model="text-embedding-v1",  # text-embedding-v3
    dashscope_api_key=os.getenv('API_KEY')
)

db = Chroma.from_documents(texts, embeddings, persist_directory="outputs/Chroma.db")
retriever = db.as_retriever(search_kwargs={'k': 1})
docs = retriever.invoke("百年校庆")
print(docs)

# 打印结果：
