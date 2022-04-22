import sqlite3
from datetime import date, datetime


# class __Database:
#     def __init__(self) -> None:
#         self._conn = sqlite3.connect("data/database.sqlite")

class __AttendanceDB():
    def __init__(self) -> None:
        self._conn = sqlite3.connect("data/database.sqlite")
        # super().__init__()

        try:
            self._conn.execute("CREATE TABLE te5 (Roll_No int(10) not null, Date DATE, Time TIME, Attendance TINYINT);")
            self._conn.close()
        except sqlite3.OperationalError:
            pass
    
    def insert(self, roll_no, attendance):
        query = "Insert into te5(Roll_No, Date, Time, Attendance) VALUES (?,?,?,?);"
        value = (roll_no, date.today(), datetime.now().strftime("%H:%M:%S"), attendance)
        self._conn.execute(query, value)
        self._conn.commit()
    
    def close(self):
        self._conn.close()
    
    def start(self):
        self._conn = sqlite3.connect("data/database.sqlite")
    
    def get_all(self):
        return self._conn.execute("SELECT * FROM te5;").fetchall()

    def __del__(self):
        self._conn.close()


class __EmbeddingDB():
    def __init__(self) -> None:
        self._conn = sqlite3.connect("data/database.sqlite")
        # super().__init__()

        try:
            self._conn.execute("CREATE TABLE embedding (Roll_No int(10) not null, Id int(30) not null primary key, Embedding TINYINT);")
            self._conn.close()
        except sqlite3.OperationalError:
            pass
    
    def close(self):
        self._conn.close()
    
    def start(self):
        self._conn = sqlite3.connect("data/database.sqlite")
    
    def insert(self, roll_no, ids):
        query = "Insert into embedding(Roll_no, Id, Embedding) VALUES (?, ?, 1);"
        data = (roll_no, ids)
        self._conn.execute(query, data)
        self._conn.commit()
    
    def get_all(self):
        return self._conn.execute("SELECT * FROM embedding;").fetchall()
    
    def find_id(self, ids):
        query = "SELECT * FROM embedding WHERE Id=?;"
        value = (ids,)
        return self._conn.execute(query, value).fetchone()
    
    def find_roll(self, roll):
        query = "SELECT * FROM embedding WHERE Roll_No=?;"
        value = (roll,)
        return self._conn.execute(query, value).fetchone()
    
    def update(self, ids, roll_no):
        query = "UPDATE embedding SET Roll_No=? Embedding=0 WHERE Id=?;"
        value = (roll_no, ids)
        self._conn.execute(query, value)
        self._conn.commit()

    def __del__(self):
        self._conn.close()

DBAttendance = __AttendanceDB()
DBEmbedding = __EmbeddingDB()


# if __name__ == '__main__':
#     db = EmbeddingDB()
    # db.insert(32130, 123456789)
    # roll, _, _ = db.find(123456789)
    # print(type(roll))