#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : Vincent
@Time    : 2026/3/24 11:12
@File    : _03_tool_api.py
@Function :
"""
import requests
from langchain.tools import tool
from langchain_openai import ChatOpenAI
import os
from langchain.agents import create_agent

from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parents[0] / ".env")

@tool
def get_weather(city: str):
    """查询城市天气"""
    url = "https://m459fcyb7c.re.qweatherapi.com/v7/weather/now"
    city_code_map = {
        "上海": "101020100",
        "北京": "101010100",
        "广州": "101280101",
        "深圳": "101280601",
    }
    response = requests.get(url, params={
        "location": city_code_map.get(city, "101280601"),
    }, headers={"X-QW-Api-Key": os.getenv("WEATHER_KEY")})
    # return f"{city} 当前天气：晴天 25℃"  # 模拟
    return response.json()


llm = ChatOpenAI(
    model="qwen-max",
    api_key=os.getenv('API_KEY'),
    base_url=os.getenv("BASE_URL"),
)

agent = create_agent(
    model=llm,
    tools=[get_weather],
    system_prompt="你是系统助手，需要根据用户的输入决定是否调用工具完成任务"
)

messages = agent.invoke({
    "messages": [{"role": "user", "content": "上海的天气怎么样？"}]
})
print(messages)
