import os
import time
import requests
import numpy as np
# from langchain_community.vectorstores import Chroma
from langchain_chroma import Chroma
from langchain_core.embeddings import Embeddings
from document_processing import load_documents, split_documents
from config import VECTOR_DB_DIR
from typing import List
import re



API_KEY = ""  #个人密钥

# 定义 MockClient 类
class MockClient:
    class EmbeddingsResponse:
        class DataItem:
            def __init__(self, text):
                # 简单的哈希模拟向量生成
                np.random.seed(hash(text) % 100)
                self.embedding = np.random.randn(768).tolist()

        def __init__(self, texts):
            self.data = [self.DataItem(text) for text in texts]

    class Embeddings:
        def create(self, model, input):
            return MockClient.EmbeddingsResponse(input)

    def __init__(self):
        self.embeddings = self.Embeddings()


# 修改 SCUECVectorizer 类，使其适配 MockClient
class SCUECVectorizer:
    def __init__(self, client):
        self.client = client
        self.embedding_cache = {}
        # 中南民族大学特定预处理词
        self.scuec_terms = {
            '民大': '中南民族大学',
            '校医院': '中南民族大学校医院',
            '图书馆': '中南民族大学图书馆',
            '后勤': '后勤保障处',
            '教务': '教务处',
            '学工': '学生工作处'
        }
        # 部门列表用于增强语义理解
        self.departments = [
            '后勤保障处', '教务处', '学生工作处', '研究生院', '招生就业处',
            '图书馆', '信息化建设管理处', '校医院', '财务处', '国际教育学院',
            '民族学与社会学学院', '文学与新闻传播学院', '数学与统计学学院',
            '计算机学院', '生物医学工程学院', '化学与材料科学学院'
        ]

    def preprocess_text(self, text: str) -> str:
        """中南民族大学文本预处理"""
        # 替换简称
        for short, full in self.scuec_terms.items():
            text = text.replace(short, full)

        # 标准化部门名称
        for dept in self.departments:
            if dept in text:
                text = text.replace(dept, f"中南民族大学{dept}")

        # 清理无关符号和格式
        text = re.sub(r'[\n\t\r]+', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()

        # 添加领域增强词
        if any(keyword in text for keyword in ['教学', '课程', '培养']):
            text += " 中南民族大学教学管理"
        elif any(keyword in text for keyword in ['科研', '研究', '项目']):
            text += " 中南民族大学科研工作"
        elif any(keyword in text for keyword in ['招生', '录取', '报考']):
            text += " 中南民族大学招生信息"

        return text

    def get_text_embedding(self, text: str, model: str = "embedding-v1") -> List[float]:
        """获取文本的向量化表示"""
        processed_text = self.preprocess_text(text)
        if processed_text in self.embedding_cache:
            return self.embedding_cache[processed_text]

        try:
            response = self.client.embeddings.create(
                model=model,
                input=[processed_text]
            )
            embedding = response.data[0].embedding
            self.embedding_cache[processed_text] = embedding
            return embedding
        except Exception as e:
            print(f"获取向量化表示失败: {e}")
            # 返回一个随机向量作为 fallback，避免后续处理出错
            return np.random.randn(768).tolist()

    def get_batch_embeddings(self, texts: List[str], model: str = "embedding-v1", batch_size: int = 16) -> List[List[float]]:
        """批量获取文本的向量化表示"""
        processed_texts = [self.preprocess_text(text) for text in texts]
        embeddings = []

        for i in range(0, len(processed_texts), batch_size):
            batch_texts = processed_texts[i:i + batch_size]
            try:
                response = self.client.embeddings.create(
                    model=model,
                    input=batch_texts
                )
                batch_embeddings = [item.embedding for item in response.data]
                embeddings.extend(batch_embeddings)
                for text, embedding in zip(batch_texts, batch_embeddings):
                    self.embedding_cache[text] = embedding
            except Exception as e:
                print(f"批量获取向量化表示失败: {e}")
                # 为每个失败的文本返回一个随机向量
                embeddings.extend([np.random.randn(768).tolist() for _ in batch_texts])

        return embeddings


class SCUECEmbeddings(Embeddings):
    """自定义嵌入模型实现，使用 SCUECVectorizer 获取嵌入向量"""

    def __init__(self):
        client = MockClient()
        self.vectorizer = SCUECVectorizer(client)

    def embed_documents(self, texts):
        """嵌入文档列表"""
        return self.vectorizer.get_batch_embeddings(texts)

    def embed_query(self, text):
        """嵌入查询文本"""
        return self.vectorizer.get_text_embedding(text)


def get_embeddings():
    """创建并返回自定义的 SCUEC 嵌入模型实例"""
    return SCUECEmbeddings()


def init_vector_store():
    """初始化或加载向量数据库"""
    if not os.path.exists(VECTOR_DB_DIR):
        print("创建新的向量数据库...")
        return create_vector_store()

    print("加载现有向量数据库...")
    return load_vector_store()


def create_vector_store():
    """创建新的向量数据库"""
    docs = load_documents()
    texts = split_documents(docs)

    # 创建自定义的 SCUEC 嵌入模型
    embeddings = get_embeddings()

    # 创建 Chroma 向量存储
    return Chroma.from_documents(
        documents=texts,
        embedding=embeddings,
        persist_directory=VECTOR_DB_DIR
    )


def load_vector_store():
    """加载现有向量数据库"""
    # 创建自定义的 SCUEC 嵌入模型
    embeddings = get_embeddings()

    return Chroma(
        persist_directory=VECTOR_DB_DIR,
        embedding_function=embeddings
    )