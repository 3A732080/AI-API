from claude_api import Client
import json
from datetime import datetime


cookie = '__ssid=4d68722947fa63f34e2b974836d447c; __stripe_mid=a6372f13-6fe6-477f-80e6-87a418a3670949b15b; intercom-device-id-lupk8zyo=74ec12b6-095d-4c4d-a981-4c0e62bb45a1; activitySessionId=aafeb2fb-4190-4e48-b3e6-e6e995393edc; cf_clearance=eud9stwSqpZ.gJMEvMAqZSlE13A4orecYiGB92kJPCU-1699377873-0-1-9879fbbf.28b97026.cf78a45f-0.2.1699377873; SL_G_WPT_TO=eo; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; __stripe_sid=1ec77611-853a-42c6-bf13-08b7b1b93a0ca6500f; sessionKey=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; intercom-session-lupk8zyo=NVFYSGNpd0xzL2dlNUNhRlI4M0ViRW9ZZ3JqdktsVWt4R1FPZnQvMmltWEUyb0ZGTTEzM1NRRzNuSTFjM3ZlaS0tMWphVnNHWVJhWkZaT3UrL1BoWlNHUT09--ce90e57643536fa60ce4e552221b46559c95c441; __cf_bm=mkUB_OZs7_49ZzwqnFrlm2BgdrCQFdwTd6gzxvCGtjw-1699377912-0-AUnd1Lzj/p0uBB6/LzNONhE/X8ztp7Pn6bGxpXUYRD0N707kOcl94E8aJ6B/38ZoZNX79fYzbdB5Csa7oVdAtqE='
claude_api = Client(cookie)

# conversations = claude_api.list_all_conversations()
# for conversation in conversations:
#     conversation_id = conversation['uuid']
#     print(conversation_id)

with open('./input/claude/claude-question.txt', 'r', encoding='utf-8') as file:
    # 使用 'read' 方法來讀取文件中的所有文字
    prompt = file.read()

print(prompt)

# conversation_id = "<conversation_id>" or claude_api.create_new_chat()['uuid']
conversation_id = "502cf515-b8bc-4b59-b05c-94dae8f5b6ad"
content = claude_api.send_message(prompt, conversation_id)

print(content)

# 生成一个以当前时间命名的文件名
current_time = datetime.now().strftime("%Y%m%d%H%M%S")
filename = f"./output/claude/claude-response{current_time}.json"

# 將回應寫入文件
with open(filename, 'w', encoding='utf-8') as file:
    # 使用 json.dump 函数将解析后的数据写入文件
    json.dump(content, file, ensure_ascii=False, indent=4)