import requests
import json
from datetime import datetime
from helper_fun import clean_json_string, dd, dump, load_file_content, save_content

class ChatGpt:
    def call_chat_gpt_api(self, api_key, message):
        """使用 ChatGPT API 發送單個消息並獲得回應"""
        try:
            response = requests.post(
                'https://api.openai.com/v1/chat/completions',
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {api_key}'
                },
                json={
                    'model': 'gpt-3.5-turbo',
                    'messages': message,
                    'temperature': 1,
                    'top_p': 1,
                    # 'top_k': 40
                })
            response.raise_for_status()

            return response.json()
        except requests.RequestException as e:
            dd(f"[ChatGpt] API error: {e}")

    def get_answer_sql(self, filepath):
        try:
            data = json.loads(load_file_content(filepath))
            index = len(data) - 1
            answer_text = json.loads(clean_json_string(data[index]['content']))

            return answer_text['sql']
        except Exception as e:

                return str(e)  # 直接將異常對象轉換為字符串

    def main(self, index, continue_text = None):
        # 載入 api_key
        api_key = load_file_content('./chat_gpt.env')

        messages = self.main_by_prepare(True)
        # dd(1)
        # messages = []

        if continue_text == None:
            question_text = load_file_content(f"./input/{index}_question.txt")
            messages.append({"role": "user", "content": question_text})
        else:
            messages = json.loads(load_file_content(f"./output/chat_gpt/{index}_question.json"))

            question_text = continue_text

            messages.append({
                "role": "user",
                 "content": question_text
            })

        content = self.call_chat_gpt_api(api_key, messages)

        if content and 'choices' in content and content['choices']:
            response_text = content['choices'][0].get('message', {}).get('content', '')

            messages.append({"role": "assistant", "content": response_text})

        save_content(messages, f"./output/chat_gpt/{index}_question.json")

    def main_by_prepare(self, finish = False):
        if finish == True:
            return json.loads(load_file_content(f"./input/prepare/chat_gpt/prepare_result.json"))

        # 載入 api_key
        api_key = load_file_content('./chat_gpt.env')

        # 準備的思路練題目
        lists = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        for index in lists:
            messages = []

            if index != 1:
                messages = json.loads(load_file_content(f"./input/prepare/chat_gpt/prepare_result.json"))

            cot_text = load_file_content(f"./input/prepare/{index}_cot.txt")

            messages.append({
                "role": "user",
                "content": cot_text
            })

            content = self.call_chat_gpt_api(api_key, messages)

            if content and 'choices' in content and content['choices']:
                response_text = content['choices'][0].get('message', {}).get('content', '')

                messages.append({"role": "assistant", "content": response_text})

                save_content(messages, f"./input/prepare/chat_gpt/prepare_result.json")

        return json.loads(load_file_content(f"./input/prepare/chat_gpt/prepare_result.json"))