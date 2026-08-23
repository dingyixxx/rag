#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : Vincent
@Time    : 2026/1/4 18:21
@File    : web_qa.py
@Function :
"""
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from model import llm, embeddings
from db import create_db
import streamlit as st
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

# 设置标题
st.set_page_config(page_title="物流行业信息咨询系统")
st.title("物流行业信息咨询RAG系统")

# 初始化全局变量
retriever = None


def get_retriever():
    """
    获取或创建检索器（单例模式）
    """
    global retriever
    if retriever is None:
        retriever = create_db('data/物流信息.pdf', embeddings, persist_directory='./chroma')
    return retriever


def format_docs(docs):
    """
    格式化检索到的文档
    """
    return "\n\n".join(doc.page_content for doc in docs)


def create_chain(retriever):
    """
    创建基于 RAG 的问答链（使用 LangChain Expression Language）
    """
    # 定义提示词模板
    template = """基于以下已知信息回答用户的问题。如果你不知道答案，就说你不知道，不要编造信息。

已知信息:
{context}

对话历史:
{chat_history}

问题：{question}

回答："""

    prompt = ChatPromptTemplate.from_template(template)

    # 构建 RAG 链
    rag_chain = (
            RunnablePassthrough.assign(
                context=lambda x: format_docs(retriever.invoke(x["question"])),
            )
            | prompt
            | llm
            | StrOutputParser()
    )

    return rag_chain


# 主逻辑
def main():
    """
    Streamlit 主页面的交互逻辑。
    """
    # print(f'st.session_state-->{st.session_state}')
    # 初始化会话状态
    if "messages" not in st.session_state:
        st.session_state.messages = []  # 用于保存聊天记录
    # print(f'st.session_state-->{st.session_state}')
    # 展示历史聊天记录
    for message in st.session_state.messages:
        # print(f'message["role"]-->{message["role"]}')
        with st.chat_message(message["role"]):
            st.markdown(message["content"])  # 显示消息内容

    # 接受用户输入
    if prompt := st.chat_input("请输入你的问题:"):
        # 保存用户消息到会话状态
        print(f'prompt--》{prompt}')
        st.session_state.messages.append({"role": "user", "content": prompt})

        # 显示用户输入
        with st.chat_message("user"):
            st.markdown(prompt)

        # 调用模型获取回答
        with st.chat_message("assistant"):
            # 占位符用于显示逐字生成的回答
            message_placeholder = st.empty()
            full_response = ""

            # 获取检索器并创建链
            retriever = get_retriever()
            chain = create_chain(retriever)

            # 准备对话历史
            chat_history_str = ""
            if len(st.session_state.messages) > 1:
                # 构建对话历史字符串
                history_messages = st.session_state.messages[:-1]  # 排除当前最新消息
                for i in range(0, min(len(history_messages), 6), 2):  # 最近 3 轮对话
                    if i + 1 < len(history_messages):
                        user_msg = history_messages[i]
                        ai_msg = history_messages[i + 1]
                        if user_msg["role"] == "user" and ai_msg["role"] == "assistant":
                            chat_history_str += f"用户：{user_msg['content']}\nAI: {ai_msg['content']}\n"

            # 调用链获取答案
            result = chain.invoke({
                "question": prompt,
                "chat_history": chat_history_str
            })
            print(f'result--->{result}')

            assistant_response = result
            message_placeholder.markdown(assistant_response)

            # 保存回答到会话状态
            st.session_state.messages.append({"role": "assistant", "content": assistant_response})


# 运行主逻辑
if __name__ == "__main__":
    main()
