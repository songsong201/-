"""
此模块使用 Flask 框架创建一个简单的 Web 应用，
提供统一页面展示聊天和地图功能。
"""
import logging
import os
from flask import Flask, render_template, send_from_directory, request, jsonify
from qa_chain import create_qa_chain
from vector_store import init_vector_store

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 初始化 Flask 应用
app = Flask(__name__, static_folder='static', template_folder='templates')

# 配置项
class Config:
    """应用配置类"""
    DEBUG = True  # 开发阶段设为True
    HOST = '0.0.0.0'  # 允许外部访问
    PORT = 5000

app.config.from_object(Config)

# 确保必要的文件夹存在
os.makedirs('templates', exist_ok=True)
os.makedirs('static/chat', exist_ok=True)

# 初始化qa_chain
vector_store = init_vector_store()
qa_chain = create_qa_chain(vector_store)

# 然后定义路由
@app.route("/")
def index():
    """返回统一页面"""
    return render_template("index.html")

@app.route("/chat")
def chat_page():
    """返回聊天页面"""
    return send_from_directory('static/chat', 'index.html')

@app.route("/map")
def map_page():
    """返回聊天页面"""
    return send_from_directory('static/map', 'index.html')

@app.route("/about")
def about_page():
    """返回聊天页面"""
    return send_from_directory('static/about', 'index.html')

@app.route('/api/chat', methods=['POST'])
def chat_api():
    """处理聊天API请求"""
    try:
        data = request.get_json()
        question = data.get('question', '')
        
        if not question:
            return jsonify({'answer': '请提供有效的问题'}), 400
        
        # 使用qa_chain获取回答
        response = qa_chain({"query": question})
        answer = response["result"]
        
        # 添加来源信息（如果有）
        if "source_documents" in response and response["source_documents"]:
            sources = set(doc.metadata.get("source", "未知来源") for doc in response["source_documents"])
            answer += f"\n\n来源: {', '.join(sources)}"
            
        return jsonify({'answer': answer})
        
    except Exception as e:
        return jsonify({'answer': f'抱歉，处理问题时遇到错误: {str(e)}'}), 500

if __name__ == "__main__":
    app.run(
        debug=app.config['DEBUG'],
        host=app.config['HOST'],
        port=app.config['PORT']
    )