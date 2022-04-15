import sqlite3
from os import getenv
from dotenv import load_dotenv
import getpass
import os
load_dotenv()

class Database:
    def __init__(self, database_name):
        self.connection = sqlite3.connect(database_name)
        self.cursor = self.connection.cursor()

    def __del__(self):
        # Close DB
        self.connection.close()

    def create_table(self, sql: str):
        self.cursor.execute(sql)
        self.connection.commit()

    def insert(self, table, *values):
        self.cursor.execute(f"INSERT INTO {table} VALUES ({','.join(['?' for _ in values])})", values)
        self.connection.commit()

    def delete(self, table, *values):
        self.cursor.execute(f"delete from {table} WHERE Imię = ?", values)
        self.connection.commit()

    def change_value(self, table, *values):
        self.cursor.execute(f"UPDATE {table} SET skill = ? WHERE Imię = ?", values)
        self.connection.commit()

    def fetch_all(self, table, **conditions):
        # SELECT * FROM url WHERE CATEGORY=?, category 
        # SELECT * FROM ulr WHERE first_name=? AND last_name=?, first_name, last_name
        values = conditions.values()
        return self.cursor.execute(
            f"SELECT * FROM {table} WHERE ({' and '.join([f'{condition}=?' for condition in conditions])})",
            list(values)
        ) 

def create_env():
    user = (getpass.getuser())
    filename = f'c:\\Users\\{user}\\Documents\\baza.db'
    cwd = os.path.dirname(__file__) + '\\.env'
    
    try:
        open(cwd, 'r')
        
    except:
        with open(cwd, 'w') as file:
            write = f"DB_NAME='{filename}'"
            file.write(write)

create_env()