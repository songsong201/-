# document_processing.py
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from config import PDF_DIR, TEXT_SPLITTER_CONFIG

def load_documents():
    """加载PDF目录中的所有文档"""
    documents = []
    for file in os.listdir(PDF_DIR):
        if file.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(PDF_DIR, file))
            documents.extend(loader.load())
    return documents

def split_documents(docs):
    """分割文档为适合处理的文本块"""
    text_splitter = RecursiveCharacterTextSplitter(**TEXT_SPLITTER_CONFIG)
    return text_splitter.split_documents(docs)