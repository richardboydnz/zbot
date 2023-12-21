import sqlite3
import time

class SQLiteCursorContext:
    def __init__(self, db_settings):
        self.db_settings = db_settings
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = sqlite3.connect(**self.db_settings)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            if exc_type is None:
                self.conn.commit()
            else:
                self.conn.rollback()
            self.conn.close()

class SQLiteConnectionMock:
    def __init__(self, db_settings):
        self.db_settings = db_settings

    def cursor(self):
        return SQLiteCursorContext(self.db_settings)

# Usage
DB_SETTINGS = {'database': 'testdb.db'}

def bc(iterations):
    conn = SQLiteConnectionMock(DB_SETTINGS)
    with conn.cursor() as cursor:
        cursor.execute("DROP TABLE test")
        cursor.execute("CREATE TABLE IF NOT EXISTS test (id INTEGER PRIMARY KEY, data TEXT)")

    start_time = time.time()
    for i in range(iterations):
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO test (data) VALUES (?)", (f"Data {i}",))

    end_time = time.time()

    return end_time - start_time

# Running the benchmark
iterations = 10000
time_taken = bc(iterations)
print(f"Time taken for {iterations} connections: {time_taken} seconds")
