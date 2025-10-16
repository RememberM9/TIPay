from sqlite3 import connect
import json

db_file_path = "./database/data.db"

class Database:
    def __init__(self, name: str, template):
        self.__name = name
        conn = self.__conn = connect(db_file_path)
        cursor = conn.cursor()
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {name} (id INTEGER, name TEXT)")
        cursor.close()

    def getData(self):
        c = self.__conn.cursor()
        c.execute(f"SELECT * FROM {self.__name}")
        rows = c.fetchall()
        # Get column names
        column_names = [description[0] for description in c.description]
        # Convert rows to list of dictionaries
        data = [dict(zip(column_names, row)) for row in rows]
        # Print as JSON
        print(json.dumps(data, indent=2))

    def prepare(self):
        self.__conn()

    def done(self):
        # Cleanup
        self.__cursor.close()
        self.__conn.close()


db = Database("users")
db.getData()
db.done()