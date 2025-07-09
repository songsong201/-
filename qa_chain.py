from config import ERNIE_ACCESS_TOKEN
import erniebot
from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from langchain_core.language_models import BaseLLM
from langchain_core.callbacks import CallbackManagerForLLMRun
from langchain_core.outputs import LLMResult
from typing import Any, Dict, List, Optional, Sequence

# 配置 erniebot
erniebot.api_type = "aistudio"
erniebot.access_token = ERNIE_ACCESS_TOKEN

PROMPT_TEMPLATE = """
你是一个中南民族大学智能问答助手，请根据提供的上下文信息回答用户问题。
如果不知道答案，请诚实回答不知道，不要编造信息。

上下文:
{context}

问题: {question}

回答(使用中文):
"""

# 创建自定义的 LangChain LLM 包装器
class ErnieBotLLM(BaseLLM):
    """自定义 ErnieBot LLM 包装器"""
    
    model: str = "ernie-3.5"
    temperature: float = 0.6
    
    def _generate(
        self,
        prompts: List[str],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> LLMResult:
        """实现抽象方法，处理多个提示"""
        responses = []
        for prompt in prompts:
            response = erniebot.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=self.temperature,
                **kwargs
            )
            responses.append([{"text": response.result}])
        
        return LLMResult(generations=responses)
    
    @property
    def _llm_type(self) -> str:
        return "erniebot"

def create_qa_chain(vector_store):
    """创建检索增强生成问答链"""
    # 创建提示模板
    prompt = PromptTemplate(
        template=PROMPT_TEMPLATE, 
        input_variables=["context", "question"]
    )
    
    # 使用自定义的 ErnieBot LLM 包装器
    llm = ErnieBotLLM()
    
    # 使用 from_chain_type 方法创建检索问答链
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_store.as_retriever(),
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=True
    )
    
    return qa_chain

def answer_question(question, qa_chain):
    """处理用户查询"""
    response = qa_chain.invoke({"query": question})
    
    # 提取答案和来源
    answer = response["result"]
    sources = list(set([doc.metadata["source"] for doc in response["source_documents"]]))
    
    # 格式化来源显示
    source_info = "\n\n来源: " + ", ".join(sources) if sources else ""
    
    return answer + source_info