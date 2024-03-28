from pymssql_fun import DatabaseConnection
from google_gemini import GoogleGemini
from chat_gpt import ChatGpt
from claude import Claude
from db_sim_fun import compare_sql_structure, compare_results
from helper_fun import clean_json_string, dd, dump, load_file_content, error_format_text, is_string
import time

# 選擇題目
lists = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

def analyze_and_compare(lists):
    # 初始化分析工具
    analyzers = {
        'google_gemini': GoogleGemini(),
        'chat_gpt': ChatGpt(),
        'claude': Claude()
    }

    res = {
        'chat_gpt': {
            'compare_res': 0,
            'structure_res': 0,
            'corrected_success': 0,
            'error_count': 0,
        },
        'google_gemini': {
            'compare_res': 0,
            'structure_res': 0,
            'corrected_success': 0,
            'error_count': 0,
        },
        'claude': {
            'compare_res': 0,
            'structure_res': 0,
            'corrected_success': 0,
            'error_count': 0,
        }
    }

    # 逐一分析各答案請求
    for i in lists:
        # 連線 MS SQL
        db = DatabaseConnection('mssql:1433', 'sa', 'YourStrong!Passw0rd', f"{i}_answer")

        # 參考答案
        dump(f"---------------------------------------------")
        dump(f"{i}_answer:")
        dump(f"---------------------------------------------")
        standard_answer = load_file_content(f"./input/{i}_answer.txt")
        dump(f"參考答案的 SQL:")
        dump(f"{standard_answer}")
        standard_results = db.query(standard_answer)
        dump(f"參考答案的SQL撈取結果: {standard_results}")

        for name, analyzer in analyzers.items():
            time.sleep(1)

            error = False
            compare_res = -1
            analyzer.main(i)
            # 分析答案
            dump(f"---------------------------------------------")
            answer_sql = analyzer.get_answer_sql(f"./output/{name}/{i}_question.json")
            dump(f"{name} 預測的 SQL:")
            dump(f"{answer_sql}")

            # 執行SQL並記錄結果
            result = db.query(answer_sql)

            if is_string(result) == False:
                # 比較結果
                compare_res = compare_results(standard_results, False, result)

            if compare_res == 0:
                result = 'Wrong Answer'

            if is_string(result):
                error = True
                res[name]['error_count'] += 1

                time.sleep(1)

                analyzer.main(i, error_format_text(result))
                # 分析答案
                answer_sql = analyzer.get_answer_sql(f"./output/{name}/{i}_question.json")
                dump(f"錯誤處理後的 SQL:")
                dump(f"{answer_sql}")

            # 結構相似度分數
            score = compare_sql_structure(standard_answer, answer_sql)
            dump(f"SQL 結構相似度: {score * 100:.2f}%")

            res[name]['structure_res'] += score

            # 執行SQL並記錄結果
            result = db.query(answer_sql, False)
            dump(f"SQL 撈取結果: {result}")

            # 比較結果
            compare_res = compare_results(standard_results, True, result)

            if error == True:
                res[name]['corrected_success'] += compare_res

            res[name]['compare_res'] += compare_res

        # 關閉連接
        db.close()

    return res

lists_length =len(lists)
result = analyze_and_compare(lists)

for analyzer, scores in result.items():
    dump(f"---------------------------------------------")
    dump(f"{analyzer} 預測的 SQL 分析:")

    compare_rate = scores['compare_res'] / lists_length * 100
    structure_similarity = scores['structure_res'] / lists_length * 100

    dump(f"準確率: {compare_rate:.2f}%")
    dump(f"SQL 結構相似度: {structure_similarity:.2f}%")

    if scores['error_count'] != 0:
        structure_similarity = scores['corrected_success'] / scores['error_count'] * 100
        dump(f"錯誤處理後的準確率: {structure_similarity:.2f}%")
    else:
        dump(f"未發生錯誤")

dump(f"---------------------------------------------")