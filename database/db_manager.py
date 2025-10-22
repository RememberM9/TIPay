# Ramilo
import sqlite3 as sql

db_file_path = "./database/data.db"


# Generate SQL table creation command from a JSON-like schema
def generate_sql_table(name, schema: dict) -> str:
    json_to_sql_typemap = {
        "str": "TEXT",  # e.g. "name": "Rem"
        "float": "REAL",  # e.g. "score": 98.6
        "int": "INTEGER",  # e.g. "id": 123
        "bool": "NUMERIC",  # e.g. "is_active": true → stored as 0 or 1
        "None": "NULL",  # e.g. "deleted_at": null
        # "dict": "TEXT",  # e.g. "profile": {...} → serialized as JSON string
        # "list": "TEXT",  # e.g. "tags": ["modular", "overlay"] → serialized as JSON string
    }
    columns = []
    id = ""
    if "id" not in schema or type(schema["id"]) is not int:
        schema["id"] = 0
        print("Warning: 'id' field missing or not int in schema. Added default 'id' as int.")

    for key, value in schema.items():
        sql_type = json_to_sql_typemap[type(value).__name__]
        if key != "id":
            columns.append(f"{key} {sql_type}")
        else:
            id = f"{key} {sql_type} PRIMARY KEY AUTOINCREMENT"

    columns = ",\n  ".join([id] + columns)
    return f"CREATE TABLE IF NOT EXISTS {name} (\n  {columns}\n)"


class Database:
    def __init__(self, name: str, template: dict):
        self.__name = name
        self.__validKeys = tuple(template.keys())
        conn = self.__conn = sql.connect(db_file_path)
        commit = self.__commit = lambda c: conn.commit() or c.close()
        cursor = conn.cursor()
        cursor.execute(generate_sql_table(name, template))
        commit(cursor)

    def getJSONData(self):
        c = self.__conn.cursor()
        c.execute(f"SELECT * FROM {self.__name}")
        rows = c.fetchall()
        # Get column names
        column_names = [description[0] for description in c.description]
        c.close()
        data = [dict(zip(column_names, row)) for row in rows]
        return data

    def has(self, id: int):
        cursor = self.__conn.cursor()
        cursor.execute(f"SELECT 1 FROM {self.__name} WHERE id = {id} LIMIT 1")
        exists = cursor.fetchone() is not None
        cursor.close()
        return exists

    def get(self, id: int):
        cursor = self.__conn.cursor()
        cursor.execute(f"SELECT * FROM {self.__name} WHERE id = {id}")
        row = cursor.fetchone()
        cursor.close()
        if row is None:
            return None
        column_names = self.__validKeys
        return dict(zip(column_names, row))

    def set(self, data: dict):
        filteredData = {}
        for k in data.keys():
            if k in self.__validKeys:
                filteredData[k] = data[k]
            else :
                print(f"Warning: Key '{k}' not in valid keys for table '{self.__name}'. Ignored.")

        cursor = self.__conn.cursor()
        sql_code = f"""
            INSERT OR REPLACE INTO {self.__name} ({",".join(filteredData.keys())})
            VALUES ({",".join(["?"] * len(filteredData))})
            """
        cursor.execute(sql_code, tuple(filteredData.values()))
        self.__commit(cursor)

    def delete(self, id: int):
        cursor = self.__conn.cursor()
        cursor.execute(f"DELETE FROM {self.__name} WHERE id = {id}")
        self.__commit(cursor)

    # empty the table items
    def clear(self):
        cursor = self.__conn.cursor()
        cursor.execute(f"DELETE FROM {self.__name}")
        self.__commit(cursor)

    def close(self):
        self.__conn.close()


# complete removal of a table in sql
def DROP(dbName: str):

    conn = sql.connect(db_file_path)
    cursor = conn.cursor()
    cursor.execute(f"DROP TABLE IF EXISTS {dbName}")
    conn.commit()
    cursor.close()
    conn.close()


# import time

# dat = {"id": 123, "name": "Remember M9", "balance": 21211.2332}
# DROP("accounts")
# db = Database("accounts", dat)

# c = 3
# while c:
#     print(db.get(123))
#     db.set(dat)
#     c -= 1
#     dat["balance"] *= 20000
#     time.sleep(1)
# db.set(dat)
# db.getJSONData()
# # db.delete(123)
# print(db.getJSONData())
# db.close()
