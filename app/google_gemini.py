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

            time.sleep(10)

        # if response.status_code != 200:
        #     dd(f"[GoogleGemini] Request failed with status code: {response.status_code}")

        response_content = response.json()['candidates'][0]['content']
        data['contents'].append(response_content)


    def get_answer_sql(self, filepath):
        try:
            data = json.loads(load_file_content(filepath))
            index = len(data) - 1
            answer_text = json.loads(clean_json_string(data[index]['parts'][0]['text']))

            return answer_text['sql']
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
