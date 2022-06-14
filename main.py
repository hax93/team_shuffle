import tkinter as tk
from os import execl
from sys import argv, executable
from threading import Thread
from tkinter import *
from tkinter import messagebox, ttk

from db_squads import *
from team_image import add_players
from team_shuffle import team_shuffle

data_db = r'src\team_select.db'
team_image = r'src\game_play.png'

class GuiSquads(ttk.Frame):
    players_play = []
    who_play_del = []
    who_play_add = []
    
    checkbox_numbers = []
    checkbox_players = {}
    list_players = {}
    
    alerts = 0

    # Add reaction buttons, labels etc.
    def __init__(self, containter):
        super().__init__(containter)
        create_db()
        self.style = ttk.Style()
        self.style.configure("Treeview.Heading", font=(None, 13))
        self.style.configure('Treeview', rowheight=25)
   
        # players get from base
        self.players_list = ttk.Treeview(self, show='headings', height=22)
        
        self.players_list['columns'] = ('Nr', 'Name', 'Rank')
        self.players_list.column('#0', width=0, stretch=YES)
        self.players_list.column('#1', anchor=CENTER, width=30)
        self.players_list.column('#2', anchor=CENTER, width=80)
        self.players_list.column('#3', anchor=CENTER, width=80)
        
        self.players_list.heading('#0', text='')
        self.players_list.heading('Nr', text="Nr", anchor=CENTER)
        self.players_list.heading('Name', text="Name", anchor=CENTER)
        self.players_list.heading('Rank', text="Rank", anchor=CENTER)  
        self.result_players_dict() 
        self.players_list.place(x=29, y=155)     
        self.players_list.focus()              
       
        # LABEL name, value
        self.title_label = Label(self, text='Name: ', font='arial 10 bold')
        self.title_label.grid(column=0, row=0, pady=5, padx=5, sticky=tk.W)
        
        self.title_label_val = Label(self, text='Value: ', font='arial 10 bold')
        self.title_label_val.grid(column=0, row=1, pady=5, padx=5, sticky=tk.W)
        
        # ENTRY add players, values
        self.add_players = StringVar()
        self.add_players_val = StringVar()
        
        self.add_players_entry = Entry(self, textvariable=self.add_players)
        self.add_players_entry_val = Entry(self, textvariable=self.add_players_val)
        
        self.add_players_entry.grid(column=0, row=0, pady=5, padx=50, sticky=tk.W)
        self.add_players_entry_val.grid(column=0, row=1, pady=5, padx=50, sticky=tk.W)
        
        self.add_players_entry.bind('<Return>', self.parse)
        self.add_players_entry_val.bind('<Return>', self.parse)
        
        # button add
        self.add_button = Button(self, text='Add', command=self.update_tree)
        self.add_button.grid(column=0, row=1, pady=0, padx=180, sticky=tk.S)
        self.add_button.bind('<Button-1>', self.parse)
        
        # results 
        self.grid(padx=10, pady=10, sticky=tk.NSEW)     
        
        #   button update, delete
        self.button_frame = LabelFrame(self, text="")
        self.button_frame.grid(padx=8, pady=20, sticky=tk.NW)

        self.update_button = Button(self.button_frame, text="Update Player", 
                               command=self.update_tree)
        self.update_button.grid(row=0, column=0, padx=10, pady=10)

        self.del_record_button = Button(self.button_frame, text="Delete Player", 
                                      command=self.record_del)
        self.del_record_button.grid(row=0, column=7, padx=10, pady=10)

        self.players_list.bind("<Double-1>", self.treeview_react_select)
        
        #   button play       
        self.button_add_players = Button(self, text='Play', font='arial 10 bold',
                                         command=lambda: [
                                             self.threading(self.exit_new_window),
                                             self.threading(self.check_marked),
                                             self.threading(self.football_field),
                                             ])
        self.button_add_players.grid(column=0, row=3, sticky=tk.W, padx=230)
       
        #   checkbuttons 
        self.vars = []
        for i in range(0, GuiSquads.checkbox_numbers[0]):
            var = StringVar()
            Checkbutton(self, text='',
                            variable=var, 
                            onvalue=i+1,
                            offvalue='off',
                            ).grid(column=0, sticky=NW) 
            self.vars.append(var)
            var.set('off')
            GuiSquads.players_play.append(f'{i+1}')

        #   restart program
        Button(self,text="Refresh",command=self.restart_program).grid()
    
    def threading(self, work):
        t1 = Thread(target=work, daemon=True)
        t1.start() 
                 
    def football_field(self):
        players, values = [], []
        prepare = [x for x in self.check_marked().values()]
        if GuiSquads.alerts <= 4 and len(self.check_marked()) <= 4:
            window_msg(self, 'info', 'Need 5 players for play game.')
            GuiSquads.alerts += 1
        elif GuiSquads.alerts >= 5 and GuiSquads.alerts < 10:
            window_msg(self, 'warning', 'Please stop doing this!')
            GuiSquads.alerts += 1
        elif GuiSquads.alerts >=10:
            window_msg(self, 'error', 'okey... Good Bye (:')
            self.quit()
        else:
            self.button_add_players['state'] = 'disabled'
            for i in prepare:
                players.append(i[0])
                values.append(i[1])
            try:
                add_players(team_shuffle(players, values))
                self.new_window = Toplevel(self)
                nw_width, nw_height = 800, 800
                
                window_position(self.new_window, nw_width, nw_height+70, divisor=1)
                
                self.image_team = PhotoImage(file=team_image)
                Label(self.new_window, image=self.image_team).pack()
                self.button_add_players['state'] = 'normal'
            except:
                window_msg(self, 'error', 'Something wrong, change some value.')
                self.button_add_players['state'] = 'normal'
        
    def exit_new_window(self):
        #   destroy window with football field
        try:
            self.new_window.destroy()
            self.new_window.update()
        except:
            pass    
            
    def restart_program(self):
         python = executable
         execl(python, python, * argv)
    
    def state(self):
        #   throw values that are marked 
        x = map((lambda var: var.get()), self.vars) 
        return x
    
    def who_play(self):
        copy = self.state()
        for i, k in enumerate(zip(GuiSquads.players_play, copy)):
            if k[0] == k[1]:
                GuiSquads.who_play_add.append(k[0])
            else:
                if (i+1) in GuiSquads.who_play_del:
                    pass
                else:
                    GuiSquads.who_play_del.append(i+1)
                    
    def check_marked(self):
        #   check who marked/not marked
        self.who_play()
        
        if len(GuiSquads.who_play_del) > 0:
            for i in GuiSquads.who_play_del:
                try:
                    del GuiSquads.checkbox_players[i]
                except:
                    pass
                
        if len(GuiSquads.who_play_add) > 0:   
            for i in GuiSquads.who_play_add:
                GuiSquads.checkbox_players[int(i)] = GuiSquads.list_players.get(int(i))
                
            GuiSquads.who_play_add.clear()
            GuiSquads.who_play_del.clear()
        return GuiSquads.checkbox_players
            
    def test_box(self):
        self.text = Text(self, height=8)
        self.text.insert('1.0', '\n'.join(GuiSquads.checkbox_players.values()))
        self.text.pack(column=0, row=0, sticky=NW)    
   
    def treeview_react_select(self, event):
        #   select record LBM
        self.select_record()
                
    def parse(self, event):
        number = int(self.add_players_entry_val.get())
        if len(self.add_players_entry.get()) >= 11:
            window_msg(self, 'error', 'Name Max 10 letters!')
        if number >= 10 or number <= 0:
            window_msg(self, 'error', 'Value only 1-9!')
        if (len(results()) + 1) > 12:
            window_msg(self, 'error', 'Only 12 players can play!')
        elif search(self.add_players.get()) is False:
            add_data(self.add_players.get(),self.add_players_val.get())
            self.add_players_entry.delete(0, END)
            self.add_players_entry_val.delete(0, END)
            self.add_players_entry.focus()
            self.result_players_dict()       
        else:
            window_msg(self, 'warning', 'Player exist.')
        
    def result_players_dict(self):
        for k, v in results().items():
            try:
                self.players_list.insert(parent='', index=k, iid=k, text='', 
                                        values=(f"{k}", f"{v[0]}", f"{v[1]}")) 
                GuiSquads.list_players[k] = [v[0], v[1]]
            except:              
                GuiSquads.list_players[k] = [v[0], v[1]]
        GuiSquads.checkbox_numbers.append(len(results().items())) 
    
    def clear_entries(self):
	    # Clear entry boxes
        self.add_players_entry.delete(0, END)
        self.add_players_entry_val.delete(0, END)
 
    def select_record(self):
        # Clear entry boxes
        self.clear_entries()
        
        # Grab record Number
        selected = self.players_list.focus()
        # Grab record values
        values = self.players_list.item(selected, 'values')

        # output to entry boxes
        self.add_players_entry.insert(0, values[1])
        self.add_players_entry_val.insert(0, values[2])
  
    def update_tree(self):  
        # Grab the record number
        selected = self.players_list.focus()
        # Update record
        self.players_list.item(selected, text="", values=('#',
                                            self.add_players_entry.get(), 
                                            self.add_players_entry_val.get()))

        db = Database(data_db)
        db.change_value('game', self.add_players_entry_val.get(), 
                        self.add_players_entry.get())
        self.result_players_dict()
    
    
    def record_del(self):
        selected = self.players_list.focus()
        values = self.players_list.item(selected, 'values')   
        del_data(values[1])
        
        x = self.players_list.selection()[0]
        self.players_list.delete(x)
        self.clear_entries()

        
def create_db():
    try:
        add_table()
    except:
        pass
                       
def window_position(self, width, height, /, divisor=2):
        scrwdth = self.winfo_screenwidth()
        scrhgt = self.winfo_screenheight()

        xLeft = int(scrwdth/divisor) - int(width/divisor)
        yTop = int(scrhgt/divisor) - int(height/divisor)
        
        return self.geometry(f"{str(width)}x{str(height)}+{str(xLeft)}+{str(yTop)}")
    
def window_msg(self, type, msg):
    if type == 'info':
        messagebox.showinfo(title='INFO', message=msg)
    elif type == 'error':
        messagebox.showerror(title='ERROR!', message=msg)
    elif type == 'warning':
        messagebox.showwarning(title='WARNING!', message=msg)
            
class App(tk.Tk):
    # config window manager
    def __init__(self):
        super().__init__()
        
        self.title('Team Shuffle')
        
        mywidth = 350
        myheight = 550
        
        window_position(self, mywidth, myheight, divisor=5)
        
        self.resizable(False, False)
  
if __name__ == '__main__':
    app = App()
    GuiSquads(app)
    app.mainloop()
