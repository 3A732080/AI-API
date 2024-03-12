import re, json
import sys, pprint

def clean_json_string(s):
    return re.sub(r'[\x00-\x1F]+', '', s)  # 將控制字符替換為空格

# helper function
def data_get(data, path, default = None):
    keys = path.split('.')
    try:
        for key in keys:
            # 加入對列表的處理
            if key.isdigit():
                data = data[int(key)]
            else:
                data = data[key]
        return data
    except (KeyError, TypeError, IndexError):
        return default

def dd(*args):
    for arg in args:
        pprint.pprint(arg, None, 1, 120)
    sys.exit()

def dump(*args):
    for arg in args:
        pprint.pprint(arg, None, 1, 120)

def load_file_content(filename):
    """讀取文件並返回內容"""
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()

def save_content(data, filepath):
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def error_format_text(text):
    return rf""" There was an error in the sql just now:
    {text}
    -------------------------------------------------------------------------------------------------------------------------------
    Please continue to reply in json format according to the above structure, without extra output and escape characters, so that I can get the MS SQL syntax for testing:
    example:

    {{
        "Description": "xxxxxxx",
        "sql": "SELECTxxxx;",
        "Explanation": "xxxxxx"
    }}
    """

def is_string(variable):
    return isinstance(variable, str)