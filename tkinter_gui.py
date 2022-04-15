import glob
from platform import platform
from tkinter import ttk
import tkinter as tk
from tkinter import *
from os import getenv
from dotenv import load_dotenv
from db_squads import Database

load_dotenv()

class GuiSquads(ttk.Frame):
    
    player_n = []
    player_name = []
    player_rank = []
    # Add reaction buttons, labels etc.
    def __init__(self, containter):
        super().__init__(containter)
        check_base()
        #self.react_button()
       
        # LABEL title, players
        self.title_label = Label(self, text='Team Selection', font='arial 10 bold')
        self.title_label.grid(column=1, row=0, padx=150, pady=0,)
        
        # players get from base
        self.players_list = ttk.Treeview(self, show='headings')
        
        self.players_list['columns'] = ('Nr', 'Name', 'Rank')
        self.players_list.column('#0', width=0, stretch=NO)
        self.players_list.column('Nr', anchor=CENTER, width=30)
        self.players_list.column('Name', anchor=CENTER, width=80)
        self.players_list.column('Rank', anchor=CENTER, width=80)
        
        self.players_list.heading('Nr', text="Nr", anchor=CENTER)
        self.players_list.heading('Name', text="Name", anchor=CENTER)
        self.players_list.heading('Rank', text="Rank", anchor=CENTER)  
        self.result_players_dict() 
        self.players_list.grid()     
        self.players_list.focus()              
       
        # ENTRY add players
        self.add_players = StringVar()
        self.add_players_val = StringVar()
        
        self.add_players_entry = Entry(self, textvariable=self.add_players)
        self.add_players_entry_val = Entry(self, textvariable=self.add_players_val)
        
        self.add_players_entry.grid(column=1, row=1, pady=20, padx=50, sticky=tk.NW)
        self.add_players_entry_val.grid(column=1, row=1, pady=65, padx=50, sticky=tk.NW)
        
        self.add_players_entry.bind('<Return>', self.parse)
        self.add_players_entry_val.bind('<Return>', self.parse)
        
        # button add
        self.add_button = Button(self, text='Add', command=self.update_tree)
        self.add_button.grid()
        self.add_button.bind('<Button-1>', self.parse)
        
        # results 
        self.grid(padx=10, pady=10, sticky=tk.NSEW)     

    def react_button(self):
        # actually trash
        self.bind('<Return>', self.parse)
        self.focus()
                
    def parse(self, event):
        add_data(self.add_players.get(),self.add_players_val.get())
        
    def result_players_dict(self):
        for k, v in results().items():
            self.players_list.insert(parent='', index=k, iid=k, text='', values=(f"{k}", f"{v[0]}", f"{v[1]}"))  
                  
    def update_tree(self):  
        selected = self.players_list.focus()
        values = self.players_list.item(selected, text="", values=self.add_players_entry.get())
        print(values)
          
# Piłka_Nożna/ zawodnicy/ Imię/ skill
def add_table():
    # dodawanie tabeli do bazy danych 
    name_sport = input("Podaj nazwe(sportu)?")
    print("Tworze tabele w bazie danych.")
    db = Database(getenv('DB_NAME'))
    db.create_table(f'''CREATE TABLE {name_sport} 
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, zawodnicy TEXT, Imię TEXT, skill VAL)''')
    # id imie skill

def check_base():
    # check base else write base

    if glob.glob(getenv('DB_NAME')):
        print("jest baza")
    else:
        print("brak bazy")
        print("Tworze baze...")
        open(getenv('DB_NAME'), 'w')
        add_table() # TUTAJ ma być tworzenie tabeli itd a nie DB xD

def add_data(players_nam, players_val):
    #   dodawanie playerów (haredzak 5)
    print("Dodaje nowe dane do bazy.")
    zawodnik = 'zawodnicy'
    imie = players_nam
    skill = players_val
    db = Database(getenv('DB_NAME'))
    db.insert('test', None, zawodnik, imie, skill)          

                
def del_data():
    #   dodawanie playerów (haredzak 5)
    dane = input("Podaj imię aby usunąć(np. haredzak):\n-")
    x = dane.split()
    print(f"Usunięto: {x}")
    imie = x[0]
    db = Database(getenv('DB_NAME'))
    db.delete('test', imie)

def set_value():
    #   zmiana wartości np (haredzak 5) na (haredzak 10)
    dane = input("Podaj imię oraz skill na który chcesz zmienić(np. haredzak 100):\n-")
    x = dane.split()
    imie = x[0]
    val = x[1]
    db = Database(getenv('DB_NAME'))
    db.change_value('test', val, imie)
    print(f"Zmiana Pozytywna.")

def results(): 
    # wyświetlanie Zawodników + Skill.
    dane = 'zawodnicy'
    db = Database(getenv('DB_NAME'))
    output = db.fetch_all('test', zawodnicy=dane)
    test = {}
    for n, i in enumerate(output):
        test[n+1] = [i[2], i[3]]
    return test

def search():
    # wyświetlanie Produkt + Cena z danej kategorii.
    dane = input("Podaj imię piłkarza:\n-")
    x = dane.split()
    names = x[0]
    db = Database(getenv('DB_NAME'))
    output = db.fetch_all('Piłka_Nożna', Imię=names)
    print(f"{names.capitalize()}".center(25 + 5, '-'))
    print()

    for n, i in enumerate(output):      
        if bytes(n) == 0:
            print("Brak takiego zawodnika")
        else:
            print(type(i))
            print(f"{n+1}.{i[2].ljust(21, '.')}{str(i[3]).rjust(5)}")
            x = f"{i[2]} {str(i[3])}"
            splajt = x.split()
            dira = list(splajt)
            print(dira)   
            
class App(tk.Tk):
    # config window manager
    def __init__(self):
        super().__init__()
        
        self.title('Team Selection')
        self.geometry('500x300')
        
if __name__ == '__main__':
    app = App()
    GuiSquads(app)
    app.mainloop()