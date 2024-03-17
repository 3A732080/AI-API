import anthropic, json
from datetime import datetime
from helper_fun import clean_json_string, dd, dump, load_file_content, save_content

class Claude:
    def add_message(self, messages, role, text):
        """添加對話到messages列表"""
        messages.append({
            "role": role,
            "content": [{"type": "text", "text": text}]
        })

    def get_answer_sql(self, filepath):
        try:
            data = json.loads(load_file_content(filepath))
            index = len(data) - 1
            answer_text = json.loads(clean_json_string(data[index]['content'][0]['text']))

            return answer_text['sql']
        except Exception as e:

                return str(e)  # 直接將異常對象轉換為字符串

    def main(self, index, continue_text = None):
        # 載入 api_key
        api_key = load_file_content('./claude.env')

        client = anthropic.Anthropic(api_key=api_key)
        messages = []


        if continue_text == None:
            question_text = load_file_content(f"./input/{index}_question.txt")
            self.add_message(messages, "user", question_text)
        else:
            messages = json.loads(load_file_content(f"./output/claude/{index}_question.json"))
            self.add_message(messages, "user", continue_text)

        # 創建對話消息
        message = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1000,
            temperature=1,
            top_p=1,
            # top_k=40,
            messages=messages
        )

        # 為了簡化，假設每個回應只有一個content block
        response_text = message.content[0].text if message.content else ""

        self.add_message(messages, "assistant", response_text)
        save_content(messages, f"./output/claude/{index}_question.json")
