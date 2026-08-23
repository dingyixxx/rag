#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : Vincent
@Time    : 2026/3/24 11:54
@File    : _02_create_agent_tools.py
@Function :
"""
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
import os
from langchain.agents import create_agent
import requests
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parents[0] / ".env")


@tool
def write_file(file_path: str, content: str):
    """
    把content写入文件路径file_path
    """
    with open(file_path, "w", encoding="utf-8") as writer:
        writer.write(content)

    print(f"写入文件{file_path} 成功")


@tool
def read_file(file_path):
    """
    读取本地文件，返回文件里的内容
    """
    with open(file_path, encoding="utf-8") as reader:
        return reader.read()


@tool
def multiply(a: int, b: int) -> int:
    """用于计算两个整数的乘积。"""
    print(f"正在执行乘法: {a} * {b}")
    return a * b


@tool
def add(a: int, b: int) -> int:
    """用于计算两个整数的乘积。"""
    print(f"正在执行加法: {a} * {b}")
    return a + b


llm = ChatOpenAI(
    model="qwen-flash",
    api_key=os.getenv('API_KEY'),
    base_url=os.getenv("BASE_URL"),
)


@tool
def get_weather(city: str):
    """查询城市天气"""
    url = "https://n567cgdrmp.re.qweatherapi.com/v7/weather/now"
    city_code_map = {
        "上海": "101020100",
        "北京": "101010100",
        "广州": "101280101",
        "深圳": "101280601",
    }
    response = requests.get(url+"?key="+os.getenv("WEATHER_KEY"), params={
        "location": city_code_map.get(city, "101280601"),
    }, headers={"X-QW-Api-Key": os.getenv("WEATHER_KEY")})
    # return f"{city} 当前天气：晴天 25℃"  # 模拟
    res=response.json()
    print(res)
    return res


tools = [get_weather, add, multiply, write_file, read_file]

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt="你是系统助手，需要根据用户的输入决定是否调用工具完成任务"
)

# messages = agent.invoke({"messages": messages})
# for each in messages["messages"]:
#     print(each)

# print(agent.invoke({"messages": HumanMessage(content="详细告诉我牛来这个电影，写入本地文件，名字自己起一个")}))

# messages = [{"role": "user", "content": "帮我算 5 * 6，然后查一下昆山的天气"}]
# messages = [{"role": "user", "content": "帮我算 5 加 6，然后读取本地的 _01_agent_search.py，总结下读取文件里面的内容"}]
messages = [{"role": "user", "content": "ai你为什么会跟我撒谎, 你会和我说你根本没有读过的书的某一章节, 你会告诉我图片里错误的球的个数,你会告诉我错误的命令行,你会告诉我错误的电影内容,你果然只是一个毫无感情毫无立场的工具"}]

# 工具的流式返回
for chunk in agent.stream({"messages": messages}):
    print(chunk)
