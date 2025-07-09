# test_ernie.py
from qa_chain import ErnieBotLLM

llm = ErnieBotLLM()
response = llm.invoke("你好，介绍一下中南民族大学")
print(response)