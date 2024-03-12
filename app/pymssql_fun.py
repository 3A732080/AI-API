import pymssql
from helper_fun import clean_json_string, dd, dump, load_file_content, save_content


class DatabaseConnection:
    _instance = None

    def __new__(cls, server, user, password, database):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance.connection = pymssql.connect(server, user, password, database)
        return cls._instance

    def __init__(self, server, user, password, database):
        self.cursor = self.connection.cursor(as_dict=True)

    def query(self, sql, exception = True):
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()

            if not results:
                return {'column': [], 'value': []}

            processed_results = []

            for row in results:
                processed_row = {'column': [], 'value': []}
                for column, value in row.items():
                    processed_row['column'].append(column)
                    processed_row['value'].append(value)
                processed_results.append(processed_row['value'])
            return {'column': processed_row['column'], 'value': processed_results}

        except pymssql.DatabaseError as e:
            if exception == False:
                return {'column': [], 'value': []}

            return str(e)  # 直接將異常對象轉換為字符串
        except pymssql.OperationalError as e:
            if exception == False:
                return {'column': [], 'value': []}

            return str(e)  # 直接將異常對象轉換為字符串
        except Exception as e:
            if exception == False:
                return {'column': [], 'value': []}

            return str(e)  # 直接將異常對象轉換為字符串

    def close(self):
        self.cursor.close()
        self.connection.close()
        DatabaseConnection._instance = None

