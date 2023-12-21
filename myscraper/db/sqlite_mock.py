import sqlite3

class SQLiteCursorContext:
    def __init__(self, db_settings):
        self.db_settings = db_settings
        self.conn = None
        self.cursor = None

    def __enter__(self) -> sqlite3.Cursor:
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
        self.closed = False

    def cursor(self) -> SQLiteCursorContext:
        if self.closed:
            raise Exception('SQLite Mock: can not create cursor on closed connection')
        else:
           return SQLiteCursorContext(self.db_settings)
    
    def close(self):
        self.closed = True

    def commit(self):
        pass

Connection = SQLiteConnectionMock
