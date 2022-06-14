import sqlite3

from team_selection import *


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
        self.cursor.execute(f"delete from {table} WHERE players = ?", values)
        self.connection.commit()

    def change_value(self, table, *values):
        self.cursor.execute(f"UPDATE {table} SET skill = ? WHERE players = ?", values)
        self.connection.commit()

    def fetch_all(self, table, **conditions):
        values = conditions.values()
        return self.cursor.execute(
            f"SELECT * FROM {table} WHERE ({' and '.join([f'{condition}=?' for condition in conditions])})",
            list(values)
        ) 
        
    def check_player(self, table, *value):
        self.cursor.execute(f"SELECT count(*) FROM {table} WHERE players == ?", value)
        self.connection.commit()
        return self.cursor.fetchone()[0]


def add_table():
    db = Database(data_db)
    db.create_table(f'''CREATE TABLE game 
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, player TEXT, players TEXT(10), skill VAL(9))''')

def add_data(players_nam, players_val):
    print("Dodaje nowe dane do bazy.")
    zawodnik = 'player'
    name = players_nam
    skill = players_val
    db = Database(data_db)
    db.insert('game', None, zawodnik, name, skill)          

                
def del_data(name):
    db = Database(data_db)
    db.delete('game', name)

def results(): 
    dane = 'player'
    db = Database(data_db)
    output = db.fetch_all('game', player=dane)

    data = {}
    for n, i in enumerate(output):
        data[n+1] = [i[2], i[3]]
    return data

def search(name):
    db = Database(data_db)
    result = db.check_player('game', name)
    if result == 0:
        return False
    else:
        return True
