from bardapi import Bard
import os
import requests
import json
from datetime import datetime


os.environ['_BARD_API_KEY'] = 'cggiS2dl8Mr4_VaBsofl1TcWLvPCAlDYAd24XtG9_IN1kppXs4RDQWUL0_UwY2DQkFiV3w.'
token='cggiS2dl8Mr4_VaBsofl1TcWLvPCAlDYAd24XtG9_IN1kppXs4RDQWUL0_UwY2DQkFiV3w.'

session = requests.Session()
session.headers = {
            "Host": "bard.google.com",
            "X-Same-Domain": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            "Origin": "https://bard.google.com",
            "Referer": "https://bard.google.com/",
        }
session.cookies.set("__Secure-1PSID", os.getenv("_BARD_API_KEY")) 
# session.cookies.set("__Secure-1PSID", token) 


bard = Bard(token=token, session=session, timeout=30)

for i in range(3):
    with open(f"./input/google-bard/google-bard-{i+1}-question.txt", 'r', encoding='utf-8') as file:
        # 使用 'read' 方法來讀取文件中的所有文字
        prompt1 = file.read()

    print(prompt1)

    res = bard.get_answer(prompt1)['content']
    print("--------------------------------------------------------------------------------------------------------------------------------------------")

    print(res)


    # 生成一个以当前时间命名的文件名
    current_time = datetime.now().strftime("%Y%m%d%H%M%S")
    filename= f"./output/google-bard/google-bard-{i+1}-response{current_time}.json"

    # 將回應寫入文件
    with open(filename, 'w', encoding='utf-8') as file:
        # 使用 json.dump 函数将解析后的数据写入文件
        json.dump(res, file, ensure_ascii=False, indent=4)