import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()


class database(object):
    def __init__(self):
        self.URL = os.environ["DATABASE_URL"]

    def connect(self):
        try:
            self.conn = psycopg2.connect(self.URL, sslmode="require")
            return print("Database Connected")
        except:
            return print("Database not Connected")

    def create_table(self):
        self.connect()
        cur = self.conn.cursor()
        cur.execute(
            """
        CREATE TABLE Compleanninator
        (
        NAME TEXT NOT NULL,
        BIRTHDAY TEXT NOT NULL,
        CHAT_ID TEXT NOT NULL
        )
        """
        )
        self.conn.commit()
        self.conn.close()
        return print("Table created")

    def insert_data(self, name, birthday, chat_id):
        self.connect()
        cur = self.conn.cursor()
        cur.execute(
            f"INSERT INTO Compleanninator (NAME, BIRTHDAY, CHAT_ID) VALUES ('{name}', '{birthday}', '{chat_id}')"
        )
        self.conn.commit()
        self.conn.close()
        return print("Data Stored")

    def delete_data(self, name, chat_id):
        self.connect()
        cur = self.conn.cursor()
        cur.execute(
            f"DELETE FROM Compleanninator WHERE (NAME, CHAT_ID) = ('{name}', '{chat_id}')"
        )
        self.conn.commit()
        self.conn.close()
        return print("Data deleted")

    def extract_data(self):
        self.connect()
        cur = self.conn.cursor()
        cur.execute("SELECT NAME, BIRTHDAY, CHAT_ID FROM Compleanninator")
        rows = cur.fetchall()
        self.conn.close()
        print(f"Data extracted: {rows}")
        return rows


db = database()
