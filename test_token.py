import erniebot
from config import ERNIE_ACCESS_TOKEN
erniebot.api_type = "aistudio"
erniebot.access_token = ERNIE_ACCESS_TOKEN

try:
    response = erniebot.ChatCompletion.create(
        model="ernie-4.5",
        messages=[{"role": "user", "content": "你好"}]
    )
    print("Token 有效！")
except Exception as e:
    print("Token 无效，请重新获取:", e)