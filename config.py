# config.py
import os
# 百度智能云API配置（从百度云控制台获取）
QIANFAN_AK = "bce-v3/ALTAK-kd0KHbq28rEiG4ZQy1GEx/e6b328129fa25ba45a91249e758c5465ac094a63"
QIANFAN_SK = "753f5acbeda543f39a5da12ff681e7fe"
# 路径配置
PDF_DIR = "knowledge"
VECTOR_DB_DIR = "./vector_db"
LOGO_PATH = "scuec_logo.png"
FAVICON_PATH = "scuec_logo.ico"
BACKGROUND_IMAGE = "background.jpg"

# 文本分割配置
TEXT_SPLITTER_CONFIG = {
    "chunk_size": 800,
    "chunk_overlap": 100,
    "separators": ["\n\n", "\n", "。", "！", "？", "；", "，", " ", ""]
}

# LLM配置
LLM_CONFIG = {
    "model": "ERNIE-Bot",
    "temperature": 0.1,
    "top_p": 0.8
}

# 检索配置
RETRIEVER_CONFIG = {
    "search_type": "similarity",
    "search_kwargs": {"k": 5}
}

ERNIE_ACCESS_TOKEN='ddebc0c6d9cf94834a08f610f62d0032fa81889f'