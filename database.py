import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()


class database(object):
    def __init__(self):
        self.PATH = os.environ["DATABASE_PATH"]

    def connect(self):  # connects to the database
        try:
            self.conn = sqlite3.connect(self.PATH)
            return print("Database Connected")
        except:
            return print("Database not Connected")

    def setup(
        self,
    ):  # creates a new BDMemo table (used manually after a reset)
        self.connect()
        cur = self.conn.cursor()
        cur.execute(
            """
        CREATE TABLE BDMemo
        (
        NAME TEXT NOT NULL,
        BIRTHDAY TEXT NOT NULL,
        CHAT_ID TEXT NOT NULL
        )
        """
        )
        cur.execute(
            """
        CREATE TABLE Settings
        (
        CHAT_ID TEXT NOT NULL,
        REMINDER_DAYS TEXT NOT NULL 
        )
        """
        )
        self.conn.commit()
        self.conn.close()
        return print("Tables created")

    def insert_data(self, name, birthday, chat_id):  # insert data into the table
        self.connect()
        cur = self.conn.cursor()
        cur.execute(
            f"INSERT INTO BDMemo (NAME, BIRTHDAY, CHAT_ID) VALUES ('{name}', '{birthday}', '{chat_id}')"
        )
        self.conn.commit()
        self.conn.close()
        return print("Data Stored")
    
    def insert_settings(self, chat_id, reminder_days):
        self.connect()
        cur = self.conn.cursor()
        cur.execute(
            f"INSERT INTO Settings (CHAT_ID, REMINDER_DAYS) VALUES ('{chat_id}', '{reminder_days}')"
        )
        self.conn.commit()
        self.conn.close()
        return print("Settings stored")

    def edit_settings(self, chat_id, reminder_days):
        self.connect()
        cur = self.conn.cursor()
        cur.execute(
            f"UPDATE Settings SET REMINDER_DAYS = '{reminder_days}' WHERE CHAT_ID = '{chat_id}'"
        )
        self.conn.commit()
        self.conn.close()
        return print(f"Settings changed: [{reminder_days}]")

    def delete_data(self, name, chat_id):  # delete data into the table
        self.connect()
        cur = self.conn.cursor()
        cur.execute(
            f"DELETE FROM BDMemo WHERE (NAME, CHAT_ID) = ('{name}', '{chat_id}')"
        )
        self.conn.commit()
        self.conn.close()
        return print("Data deleted")

    def extract_data(self):  # get all the data from the table
        self.connect()
        cur = self.conn.cursor()
        cur.execute("SELECT NAME, BIRTHDAY, CHAT_ID FROM BDMemo")
        rows = cur.fetchall()
        self.conn.close()
        print(f"Data extracted: {rows}")
        return rows
    
    def extract_settings(self):
        self.connect()
        cur = self.conn.cursor()
        cur.execute("SELECT CHAT_ID, REMINDER_DAYS FROM Settings")
        rows = cur.fetchall()
        self.conn.close()
        print("Settings extracted")
        return rows

    def get_list(self, chat_id):  # get the data stored from a user
        self.connect()
        cur = self.conn.cursor()
        cur.execute(f"SELECT NAME, BIRTHDAY FROM BDMemo WHERE CHAT_ID = '{chat_id}'")
        list = cur.fetchall()
        self.conn.close()
        return list


db = database()
