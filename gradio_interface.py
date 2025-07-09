# gradio_interface.py
import gradio as gr
from qa_chain import answer_question
from config import LOGO_PATH, FAVICON_PATH  # 添加BACKGROUND_IMAGE
import time
import random
from gradio.themes import Soft

BACKGROUND_IMAGE_PATH = "background.jpg"


def launch_gradio_interface(qa_chain):
    """创建并启动中南民族大学智能问答系统界面"""
    # 自定义CSS样式 - 优化版
    css = f"""
    :root {{
        --primary-color: #4a6fa5;
        --secondary-color: #6c91c0;
        --accent-color: #ff6b6b;
        --light-color: #f5f7fa;
        --dark-color: #2c3e50;
        --shadow: 0 4px 12px rgba(0,0,0,0.1);
        --border-radius: 16px;
    }}
    
    body {{
        background-size: cover;
        font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif;
        min-height: 100vh;
        margin: 0;
        padding: 20px;
    }}
    
    .container {{
        max-width: 800px;
        margin: 40px auto;
        background: rgba(255, 255, 255, 0.92);
        border-radius: var(--border-radius);
        box-shadow: var(--shadow);
        overflow: hidden;
        position: relative;
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }}
    
    .header {{
        background: linear-gradient(to right, rgba(74, 111, 165, 0.9), rgba(108, 145, 192, 0.9));
        color: white;
        padding: 25px 30px;
        border-radius: var(--border-radius) var(--border-radius) 0 0;
        position: relative;
    }}
    
    .header::before {{
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: var(--accent-color);
    }}
    
    .logo-title {{
        display: flex;
        align-items: center;
        gap: 15px;
    }}
    
    .logo-container {{
        width: 60px;
        height: 60px;
        background-color: white;
        border-radius: 50%;
        padding: 5px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: var(--shadow);
    }}
    
    .logo-container img {{
        max-height: 50px;
        max-width: 50px;
    }}
    
    .title {{
        font-size: 28px;
        font-weight: 700;
        letter-spacing: -0.5px;
        text-shadow: 0 1px 2px rgba(0,0,0,0.2);
    }}
    
    .subtitle {{
        margin-top: 8px;
        font-size: 16px;
        opacity: 0.95;
        max-width: 600px;
        line-height: 1.5;
        text-shadow: 0 1px 1px rgba(0,0,0,0.1);
    }}
    
    .welcome {{
        padding: 20px 30px;
        background: rgba(245, 247, 250, 0.85);
        border-bottom: 1px solid rgba(234, 234, 234, 0.6);
    }}
    
    .welcome-text {{
        font-size: 16px;
        color: var(--dark-color);
        line-height: 1.6;
        margin-bottom: 10px;
    }}
    
    .example-questions {{
        background: rgba(240, 244, 248, 0.85);
        padding: 15px 20px;
        border-radius: 8px;
        margin-top: 15px;
    }}
    
    .examples-title {{
        font-weight: 600;
        color: var(--primary-color);
        margin-bottom: 10px;
    }}
    
    .example {{
        display: inline-block;
        background: rgba(255, 255, 255, 0.9);
        border-radius: 20px;
        padding: 8px 16px;
        margin: 5px 8px 5px 0;
        font-size: 14px;
        cursor: pointer;
        transition: all 0.2s;
        border: 1px solid rgba(224, 230, 237, 0.5);
    }}
    
    .example:hover {{
        transform: translateY(-2px);
        box-shadow: 0 3px 8px rgba(0,0,0,0.1);
        border-color: var(--secondary-color);
        background: rgba(245, 249, 255, 0.95);
    }}
    
    .chat-area {{
        padding: 30px;
    }}
    
    .input-area {{
        display: flex;
        gap: 15px;
        margin-top: 20px;
    }}
    
    .question-input {{
        flex: 1;
        padding: 15px 20px;
        border-radius: 50px;
        border: 1px solid rgba(219, 225, 232, 0.7);
        font-size: 16px;
        transition: all 0.3s;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        background: rgba(255, 255, 255, 0.9);
    }}
    
    .question-input:focus {{
        border-color: var(--secondary-color);
        box-shadow: 0 4px 12px rgba(74, 111, 165, 0.2);
        outline: none;
        background: rgba(255, 255, 255, 0.95);
    }}
    
    .submit-btn {{
        background: linear-gradient(to right, var(--primary-color), var(--secondary-color));
        color: white;
        border: none;
        border-radius: 50px;
        padding: 0 30px;
        font-size: 16px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s;
        box-shadow: 0 4px 10px rgba(74, 111, 165, 0.3);
    }}
    
    .submit-btn:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 14px rgba(74, 111, 165, 0.4);
    }}
    
    .submit-btn:active {{
        transform: translateY(0);
    }}
    
    .clear-btn {{
        background: rgba(255, 255, 255, 0.9);
        color: var(--dark-color);
        border: 1px solid rgba(219, 225, 232, 0.7);
        border-radius: 50px;
        padding: 0 25px;
        font-size: 16px;
        cursor: pointer;
        transition: all 0.2s;
    }}
    
    .clear-btn:hover {{
        background: rgba(248, 250, 253, 0.95);
        border-color: rgba(193, 203, 216, 0.8);
    }}
    
    .answer-output {{
        background: rgba(255, 255, 255, 0.9);
        border-radius: 18px;
        padding: 25px;
        min-height: 200px;
        border: 1px solid rgba(224, 230, 237, 0.5);
        box-shadow: inset 0 2px 6px rgba(0,0,0,0.03);
        font-size: 16px;
        line-height: 1.7;
        color: var(--dark-color);
        overflow-y: auto;
        max-height: 400px;
    }}
    
    .answer-output:empty::before {{
        content: "等待您提出问题...";
        color: #a0aec0;
        font-style: italic;
    }}
    
    .user-msg {{
        margin-bottom: 20px;
        padding: 15px 20px;
        background: rgba(240, 247, 255, 0.85);
        border-radius: 10px;
        border-left: 4px solid var(--primary-color);
    }}
    
    .assistant-msg {{
        margin-top: 20px;
        padding: 15px 20px;
        background: rgba(249, 249, 249, 0.85);
        border-radius: 10px;
        border-left: 4px solid var(--secondary-color);
    }}
    
    .footer {{
        display: flex;
        justify-content: space-between;
        padding: 15px 30px;
        background: rgba(245, 247, 250, 0.85);
        border-top: 1px solid rgba(234, 234, 234, 0.6);
        border-radius: 0 0 var(--border-radius) var(--border-radius);
    }}
    
    .powered-by {{
        color: #718096;
        font-size: 14px;
    }}
    
    .footer-buttons {{
        display: flex;
        gap: 10px;
    }}
    
    .footer-btn {{
        background: rgba(255, 255, 255, 0.9);
        color: var(--dark-color);
        border: 1px solid rgba(219, 225, 232, 0.7);
        border-radius: 20px;
        padding: 8px 20px;
        font-size: 14px;
        cursor: pointer;
        transition: all 0.2s;
    }}
    
    .footer-btn:hover {{
        background: rgba(248, 250, 253, 0.95);
        border-color: rgba(193, 203, 216, 0.8);
    }}
    
    .thinking {{
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 20px;
        color: #718096;
        font-style: italic;
        background: rgba(249, 249, 249, 0.85);
        border-radius: 10px;
        margin-top: 10px;
    }}
    
    .thinking::after {{
        content: ".";
        animation: dots 1.5s infinite;
        width: 10px;
        display: inline-block;
        text-align: left;
    }}
    
    @keyframes dots {{
        0%, 20% {{ content: "."; }}
        40% {{ content: ".."; }}
        60%, 100% {{ content: "..."; }}
    }}
    
    .timestamp {{
        font-size: 12px;
        color: #718096;
        text-align: right;
        margin-top: 5px;
    }}
    
    .response-time {{
        font-size: 14px;
        color: #718096;
        text-align: right;
        margin-top: 10px;
        font-style: italic;
    }}
    """
    
    # 示例问题列表
    example_questions = [
        "电子信息工程学院的课本领取地点在哪里？",
        "明天天气怎么样？适合户外活动吗？",
        "图书馆的开放时间是？",
        "校园卡如何充值？有哪些方式？",
        "计算机科学专业的核心课程有哪些？",
        "学校附近有哪些好吃的餐厅？",
        "如何申请宿舍调换？",
        "学校的奖学金有哪些类型？",
        "体育馆的开放时间是什么时候？",
        "学校有哪些社团可以参加？"
    ]
    
    # 获取当前时间
    def get_current_time():
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    
    # 定义处理用户问题的函数
    def respond(message, history_html):
        """处理用户查询并返回答案"""
        if not message.strip():
            return history_html, ""
        
        # 获取当前时间
        current_time = get_current_time()
        
        # 添加用户问题到历史
        user_message = f"""
        <div class="user-msg">
            <div><strong>👤 您</strong> · <span class="timestamp">{current_time}</span></div>
            <div style="margin-top: 8px;">{message}</div>
        </div>
        """
        updated_history = history_html + user_message
        
        # 显示思考状态
        thinking_messages = [
            "正在查阅校园知识库...",
            "正在分析您的问题...",
            "正在整理最佳答案..."
        ]
        thinking_message = f"""
        <div class="thinking">
            <strong>小塔:</strong> {random.choice(thinking_messages)}
        </div>
        """
        yield updated_history + thinking_message, ""
        
        # 获取答案
        start_time = time.time()
        try:
            response = qa_chain({"query": message})
            answer = response["result"]
            
            # 添加来源信息（如果有）
            if "source_documents" in response and response["source_documents"]:
                sources = set(doc.metadata.get("source", "未知来源") for doc in response["source_documents"])
                source_info = "<br><div style='font-size: 14px; color: #718096; margin-top: 10px;'>来源: " + ", ".join(sources) + "</div>"
                answer += source_info
                
        except Exception as e:
            answer = f"抱歉，处理问题时遇到错误: {str(e)}"
        elapsed = time.time() - start_time
        
        # 格式化答案
        formatted_response = f"""
        <div class="assistant-msg">
            <div><strong>🤖 小塔</strong> · <span class="timestamp">{get_current_time()}</span></div>
            <div style="margin-top: 8px;">{answer}</div>
            <div class="response-time">回答耗时: {elapsed:.2f}秒</div>
        </div>
        """
        
        # 更新历史记录（移除思考消息，添加最终回复）
        final_history = updated_history + formatted_response
        yield final_history, ""
    
    # 创建Blocks界面
    with gr.Blocks(
        css=css,
        title="中南民大智能问答助手",
        # 借助 gradio 方式设置背景
        theme=gr.themes.Default().set(
            body_background_fill=f"url('file={BACKGROUND_IMAGE_PATH}') no-repeat center center fixed"
        )
    ) as demo:
        with gr.Column(elem_classes="container"):
            # 顶部标题区域
            with gr.Column(elem_classes="header"):
                with gr.Row(elem_classes="logo-title"):
                    with gr.Column(scale=1, min_width=80):
                        with gr.Row():
                            with gr.Column(min_width=70):
                                gr.HTML(
                                    f"<div class='logo-container'><img src='file={LOGO_PATH}' alt='小塔'></div>"
                                )
                    with gr.Column(scale=4):
                        gr.Markdown(
                            "<div class='title'>小塔 - 中南民大智能助手</div>"
                            "<div class='subtitle'>您的专属校园助手，回答任何问题，帮助您更快适应校园生活</div>",
                            elem_id="title-area"
                        )
            
            # 欢迎区域
            with gr.Column(elem_classes="welcome"):
                gr.Markdown(
                    "<div class='welcome-text'>"
                    "👋 您好！我是小塔，中南民族大学的智能问答助手。"
                    "我可以回答您关于学校生活、课程安排、校园设施等各种问题。"
                    "欢迎随时向我提问！"
                    "</div>"
                )
                
                with gr.Column(elem_classes="example-questions"):
                    gr.Markdown("<div class='examples-title'>您可以尝试问我：</div>")
                    
                    # 动态生成示例问题
                    with gr.Row():
                        examples_html = "<div>"
                        for i, question in enumerate(example_questions[:4]):
                            examples_html += f"<div class='example' id='example-{i}'>{question}</div>"
                        examples_html += "</div>"
                        examples_container = gr.HTML(examples_html)
                    
                    with gr.Row():
                        examples_html2 = "<div>"
                        for i, question in enumerate(example_questions[4:8]):
                            examples_html2 += f"<div class='example' id='example-{i+4}'>{question}</div>"
                        examples_html2 += "</div>"
                        examples_container2 = gr.HTML(examples_html2)
            
            # 聊天区域
            with gr.Column(elem_classes="chat-area"):
                # 聊天历史记录
                history_html = gr.HTML(
                    value="", 
                    elem_classes="answer-output",
                    label="对话历史"
                )
                
                # 输入区域
                with gr.Row(elem_classes="input-area"):
                    question_input = gr.Textbox(
                        placeholder="请输入您的问题，例如：中南民族大学有哪些优势学科？",
                        lines=2,
                        elem_classes="question-input",
                        label="",
                        show_label=False
                    )
                    submit_btn = gr.Button("发送", elem_classes="submit-btn")
            
            # 底部区域
            with gr.Row(elem_classes="footer"):
                gr.Markdown("<div class='powered-by'>Powered by 中南民族大学 & ErnieBot AI</div>")
                with gr.Column(elem_classes="footer-buttons"):
                    clear_btn = gr.Button("清空对话", elem_classes="footer-btn")
        
        # 事件处理 - 用户输入
        question_input.submit(
            fn=respond,
            inputs=[question_input, history_html],
            outputs=[history_html, question_input]
        )
        
        submit_btn.click(
            fn=respond,
            inputs=[question_input, history_html],
            outputs=[history_html, question_input]
        )
        
        # 事件处理 - 清空对话
        clear_btn.click(
            fn=lambda: ["", ""],
            inputs=[],
            outputs=[history_html, question_input]
        )
        
        # 事件处理 - 示例问题点击
        js_code = """
        function setupExampleListeners() {
            document.querySelectorAll('.example').forEach(element => {
                element.addEventListener('click', function() {
                    const question = this.textContent;
                    const textarea = document.querySelector('.question-input textarea');
                    if (textarea) {
                        textarea.value = question;
                        // 触发输入事件以便Gradio检测到变化
                        const event = new Event('input', { bubbles: true });
                        textarea.dispatchEvent(event);
                        
                        // 可选：自动聚焦到输入框
                        textarea.focus();
                    }
                });
            });
        }
        
        // 初始设置
        setTimeout(setupExampleListeners, 1000);
        
        // 当Gradio重新渲染时重新设置
        document.addEventListener('render', function() {
            setTimeout(setupExampleListeners, 1000);
        });
        """
        
        demo.load(
            fn=None,
            inputs=None,
            outputs=None,
            js=js_code
        )
    
    # 启动界面
    demo.launch(
        server_name="localhost",
        server_port=7860,
        favicon_path=FAVICON_PATH,
        share=False
    )