import json
import requests
from datetime import datetime
from helper_fun import clean_json_string, dd, dump, load_file_content, save_content
import os, time

class GoogleGemini:
    def add_question_to_data(self, data, filepath):
        data['contents'].append({
            "role": "user",
            "parts": [{"text": load_file_content(filepath)}]
        })

    def send_request_and_process_response(self, session, url, headers, data):
        status = 0

        while (status != 200):
            response = session.post(url, headers=headers, json=data)

            status = response.status_code

            time.sleep(1)

        # if response.status_code != 200:
        #     dd(f"[GoogleGemini] Request failed with status code: {response.status_code}")

        response_content = response.json()['candidates'][0]['content']
        data['contents'].append(response_content)


    def get_answer_sql(self, filepath):
        try:
            data = json.loads(load_file_content(filepath))
            answer_text = json.loads(clean_json_string(data[-1]['parts'][0]['text']))

            return answer_text['sql']
        except Exception as e:
            try:
                # 從原始字符串中移除 Markdown 語法，只保留 JSON 部分
                answer_text = json.loads(clean_json_string(data[-1]['parts'][0]['text'])[7:-3])

                return answer_text["sql"].replace("\\n", "\n")
            except Exception as e:
                return str(e)  # 直接將異常對象轉換為字符串

    def main(self, index, continue_text = None):
        api_key = load_file_content('./google_gemini.env')
        session = requests.Session()

        url = f'https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={api_key}'
        headers = {'Content-Type': 'application/json'}
        data = {
            "contents": [],
            "generationConfig": {
                "temperature": "1",
                "topP": "1",
                # "topK": "40",
                # "candidateCount": "<integer>",
                # "maxOutputTokens": "<integer>",
                # "stopSequences": ["<string>"]
            }
        }

        data['contents'] = self.main_by_prepare(True)
        # dd(1)

        if continue_text == None:
            self.add_question_to_data(data, f"./input/{index}_question.txt")
        else:
            data['contents'] = json.loads(load_file_content(f"./output/google_gemini/{index}_question.json"))
            data['contents'].append({
                "role": "user",
                "parts": [{"text": continue_text}]
            })

        self.send_request_and_process_response(session, url, headers, data)

        save_content(data['contents'], f"./output/google_gemini/{index}_question.json")


    def main_by_prepare(self, finish = False):
        if finish == True:
            return json.loads(load_file_content(f"./input/prepare/google_gemini/prepare_result.json"))

        api_key = load_file_content('./google_gemini.env')
        session = requests.Session()

        url = f'https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={api_key}'
        headers = {'Content-Type': 'application/json'}
        data = {
            "contents": [],
            "generationConfig": {
                "temperature": "1",
                "topP": "1",
                # "topK": "40",
                # "candidateCount": "<integer>",
                # "maxOutputTokens": "<integer>",
                # "stopSequences": ["<string>"]
            }
        }

        # 準備的思路練題目
        lists = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        for index in lists:
            if index != 1:
                data['contents'] = json.loads(load_file_content(f"./input/prepare/google_gemini/prepare_result.json"))

            self.add_question_to_data(data, f"./input/prepare/{index}_cot.txt")

            self.send_request_and_process_response(session, url, headers, data)

            save_content(data['contents'], f"./input/prepare/google_gemini/prepare_result.json")

        return json.loads(load_file_content(f"./input/prepare/google_gemini/prepare_result.json"))
