# 校园智慧问答助手应用
## SCUEC-AgentChat

# 项目结构
```angular2html
|-- config.py
|-- document_processing.py
|-- qa_chain.py
|-- vector_store.py
|-- static
|-- chat
    |--index.html
|-- map
    |--index.html
|-- about
    |--index.html
|-- image
    |--图书馆.png
    |--.......png
|-- templates
|-- index.html
|-- LocalAgent
    |-- LLM-Ernie3.5
        |-- RAG
        |-- tools
    |-- view
        |--Flask
```
# QuickStart

安装依赖，需要 Python 3.10 以上版本。

```
pip install -r requirements.txt
```

授权

```
config中包含aistudio的令牌token-调用Ernie-3.5
```



启动

```
python app.py
```

### 功能实现：

- 智慧问答：
  - 关于校园的全部问题
- 地图
  - 校园地图和建筑图片
  - 3D全景地图
- RAG检索增强
  - 自定义上传文件处理形成向量知识库
