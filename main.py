# main.py
from gradio_interface import launch_gradio_interface
from vector_store import init_vector_store
from qa_chain import create_qa_chain
import webbrowser

# 初始化问答系统
print("加载现有向量数据库...")
vector_store = init_vector_store()
qa_chain = create_qa_chain(vector_store)

# 启动Gradio界面
print("正在启动问答系统界面...")
launch_gradio_interface(qa_chain)

# 添加自动打开浏览器的功能
print("尝试在浏览器中打开界面...")
webbrowser.open("http://localhost:7860")