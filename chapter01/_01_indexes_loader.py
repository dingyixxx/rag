#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : Vincent
@Time    : 2026/1/4 17:46
@File    : _01_indexes_loader.py
@Function :
"""
# from langchain_community.document_loaders import UnstructuredFileLoader
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parents[0] / ".env")

from langchain_unstructured import UnstructuredLoader

# 创建一个加载器
loader = UnstructuredLoader('data/衣服属性.txt', encoding='utf8')
# 加载
docs = loader.load()  # 返回是列表 List[Document]
print(docs)
print(len(docs))
first_01 = docs[0].page_content[:10]
print(first_01)
print('*' * 80)

from langchain_community.document_loaders import TextLoader

loader = TextLoader('data/衣服属性.txt', encoding='utf8')
docs = loader.load()  # 返回是列表 List[Document]
print(docs)
print(len(docs))
first_01 = docs[0].page_content[:10]
print(first_01)

# 打印结果：
'''
[Document(page_content='身高：160-170cm， 体重：90-115斤，建议尺码M。\n身高：165-175cm， 体重：115-135斤，建议尺码L。\n身高：170-178cm， 体重：130-150斤，建议尺码XL。\n身高：175-182cm， 体重：145-165斤，建议尺码2XL。\n身高：178-185cm， 体重：160-180斤，建议尺码3XL。\n身高：180-190cm， 体重：180-210斤，建议尺码4XL。\n面料分类：其他\n图案：纯色\n领型：翻领\n衣门襟：单排扣\n颜色：黑色 卡其色 粉色 杏色\n袖型：收口袖\n适用季节：冬季\n袖长：长袖\n厚薄：厚款\n适用场景：其他休闲\n衣长：常规款\n版型：宽松型\n款式细节：假两件\n工艺处理：免烫处理\n适用对象：青年\n面料功能：保暖\n穿搭方式：外穿\n销售渠道类型：纯电商(只在线上销售)\n材质成分：棉100%', metadata={'source': '衣服属性.txt'})]
1
身高：1
********************************************************************************
[Document(page_content='身高：160-170cm， 体重：90-115斤，建议尺码M。\n\n身高：165-175cm， 体重：115-135斤，建议尺码L。\n\n身高：170-178cm， 体重：130-150斤，建议尺码XL。\n\n身高：175-182cm， 体重：145-165斤，建议尺码2XL。\n\n身高：178-185cm， 体重：160-180斤，建议尺码3XL。\n\n身高：180-190cm， 体重：180-210斤，建议尺码4XL。\n\n面料分类：其他\n\n图案：纯色\n\n领型：翻领\n\n衣门襟：单排扣\n\n颜色：黑色 卡其色 粉色 杏色\n\n袖型：收口袖\n\n适用季节：冬季\n\n袖长：长袖\n\n厚薄：厚款\n\n适用场景：其他休闲\n\n衣长：常规款\n\n版型：宽松型\n\n款式细节：假两件\n\n工艺处理：免烫处理\n\n适用对象：青年\n\n面料功能：保暖\n\n穿搭方式：外穿\n\n销售渠道类型：纯电商(只在线上销售)\n\n材质成分：棉100%', metadata={'source': '衣服属性.txt'})]
1
身高：1
'''
