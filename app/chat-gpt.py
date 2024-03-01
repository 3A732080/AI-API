import requests
import json
from datetime import datetime

# 1. 使用request模組來串接API

with open('./chat-gpt.env', 'r', encoding='utf-8') as file:
    # 使用 'read' 方法來讀取文件中的所有文字
    api_key = file.read()

with open('./input/chat-gpt/chat-gpt-question.txt', 'r', encoding='utf-8') as file:
    # 使用 'read' 方法來讀取文件中的所有文字
    prompt = file.read()

print(prompt)

response = requests.post(
    'https://api.openai.com/v1/chat/completions',
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    },
    json = {
        'model': 'gpt-3.5-turbo', # 一定要用chat可以用的模型
        'messages' : [{"role": "user", "content": prompt}]
    })

# #使用json解析
content = response.json()
print(content)

# 生成一个以当前时间命名的文件名
current_time = datetime.now().strftime("%Y%m%d%H%M%S")
filename = f"./output/chat-gpt/chat-gpt-response{current_time}.json"

# 將回應寫入文件
with open(filename, 'w', encoding='utf-8') as file:
    # 使用 json.dump 函数将解析后的数据写入文件
    json.dump(content, file, ensure_ascii=False, indent=4)
