import tkinter as tk
from tkinter import Tk, Frame, Menu, ttk, Label, Entry, Button, messagebox
from tkinter import ttk
import psycopg2
from host import host, user, password, db_name
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# connection = psycopg2.connect( host=host, user=user, password=password, database=db_name)
# cur = connection.cursor()
class DB_menu(Frame):
 
    def __init__(self):
        super().__init__()
        self.initUI()
 
    def initUI(self):
        #self.master.title("Простое меню")
 
        menubar = Menu(self.master)
        self.master.config(menu=menubar)
 
        fileMenu = Menu(menubar)
        fileMenu.add_command(label="Удалить базу данных", command=self.drop_db)
        fileMenu.add_command(label="Подключиться к базе данных другой школы", command=self.connect_any)
        
        fileMenu2 = Menu(menubar)
        fileMenu2.add_command(label="Очистить все таблицы", command= lambda: [self.delete_tab1(), self.delete_tab2(), self.delete_tab3(), self.delete_tab4()])
        fileMenu2.add_command(label="Очистить таблицу \"Члены клуба\"", command=self.delete_tab1)
        fileMenu2.add_command(label="Очистить таблицу \"Лучшие приемы\"", command=self.delete_tab2)
        fileMenu2.add_command(label="Очистить таблицу \"Статистика игрока\"", command=self.delete_tab3)
        fileMenu2.add_command(label="Очистить таблицу \"Матчи\"", command=self.delete_tab4)

        menubar.add_cascade(label="Таблица", menu=fileMenu2)
        menubar.add_cascade(label="База данных", menu=fileMenu)
        
       
    def delete_tab1(self):
        # self.quit()
        connection = psycopg2.connect( host=host, user=user, password=password, database=db_name)
        cur = connection.cursor()
        cur.execute("TRUNCATE members")
        connection.commit()
        cur.close()
        connection.close()
    def delete_tab2(self):
        # self.quit()
        connection = psycopg2.connect( host=host, user=user, password=password, database=db_name)
        cur = connection.cursor()
        cur.execute("TRUNCATE Best_tricks")
        connection.commit()
        cur.close()
        connection.close()
    def delete_tab3(self):
        # self.quit()
        connection = psycopg2.connect( host=host, user=user, password=password, database=db_name)
        cur = connection.cursor()
        cur.execute("TRUNCATE player_statistics")
        connection.commit()
        cur.close()
        connection.close()
    def delete_tab4(self):
        # self.quit()
        connection = psycopg2.connect( host=host, user=user, password=password, database=db_name)
        cur = connection.cursor()
        cur.execute("TRUNCATE matches")
        connection.commit()
        cur.close()
        connection.close()
        
    def connect_any(self):
        self.master2 = Tk()
        self.master2.title("Введите название школы")
        self.master2.geometry("300x100+300+200")
        self.master2.resizable(False, False)
        e = Entry(self.master2)
        e.pack()

        e.focus_set()

        b = Button(self.master2, text = "Подключиться", width = 15, command= lambda: self.connect_school(e.get()))
        b.pack()
        
    def drop_db(self):
        con = psycopg2.connect( host=host, user=user, password=password, database="postgres")
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT) # <-- ADD THIS LINE
        self.db_name = db_name
        self.cur = con.cursor()
        self.cur.execute(sql.SQL(f"DROP DATABASE {self.db_name}"))
    
    def connect_school(self, e):
        con = psycopg2.connect( host=host, user=user, password=password, database="postgres")
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT) # <-- ADD THIS LINE

        self.cur = con.cursor()
        self.cur.execute("SELECT * FROM pg_catalog.pg_database WHERE datname = %s", (e,))
        flag = self.cur.fetchone()
        if flag is None:
            self.cur.execute(sql.SQL("CREATE DATABASE {}").format(
                sql.Identifier(e)))
            connection = psycopg2.connect( host=host, user=user, password=password, database=e)
            cur = connection.cursor()
            cur.execute("CREATE TABLE members(Member_id INTEGER PRIMARY KEY,First_Name CHARACTER VARYING(30) NOT NULL,Last_Name CHARACTER VARYING(30) NOT NULL,Date_of_Birth DATE NOT NULL,Height INTEGER,Position_ CHARACTER VARYING(30),Number_ INTEGER); ")
            cur.execute("CREATE TABLE Best_tricks (Trick_name CHARACTER VARYING(30) NOT NULL,Description CHARACTER VARYING(100) NOT NULL,Main_performer INTEGER)")
            cur.execute("CREATE TABLE player_statistics (Player_id INTEGER PRIMARY KEY,Strength INTEGER,Jumping INTEGER,Endurance INTEGER,Strategy INTEGER,Technique INTEGER,Speed INTEGER, irreplaceable INTEGER DEFAULT 1)")
            cur.execute("CREATE TABLE matches (competitions_name CHARACTER VARYING(30) NOT NULL,enemy CHARACTER VARYING(30) NOT NULL,Date DATE NOT NULL,Result CHARACTER VARYING(30), CONSTRAINT matches_key PRIMARY KEY (enemy, date))")
            cur.execute("create or replace function IRREPLACEABLE() returns trigger as $u$ begin  update player_statistics set irreplaceable = (SELECT COUNT(main_performer) FROM Best_tricks Where Player_id = Main_performer); return new; end; $u$ language plpgsql; drop trigger if exists trigger_IRREPLACEABLE on Best_tricks; create trigger trigger_IRREPLACEABLE after insert or update OR DELETE on Best_tricks for EACH row execute procedure IRREPLACEABLE(); ")
            connection.commit()
            cur.close()
            connection.close()
        else:
            connection = psycopg2.connect( host=host, user=user, password=password, database=e)
            cur = connection.cursor()
            cur.close()
            connection.close()
        global db_name 
        db_name = e
        self.master2.destroy()

def button_table_1_click(id_e,name_entry, name2_entry, dateb_entry,height_entry, Position_entry, Number_):
    if name_entry != "" and name2_entry != "" and dateb_entry != "" and height_entry != "" and Position_entry != "":
        connection = psycopg2.connect( host=host, user=user, password=password, database=db_name)
        cur = connection.cursor()
        cur.execute("INSERT INTO Members (member_id, First_Name, Last_Name, Date_of_Birth, Height, Position_, Number_) VALUES (%s, %s, %s, %s, %s, %s, %s)", (id_e, name_entry, name2_entry, dateb_entry,height_entry, Position_entry, Number_))
        connection.commit()
        cur.close()
        connection.close()
        #Frame.name_entry.delete(0, "END")
        #name2_entry.delete(0, "END")
    else:
        messagebox.showinfo("Ошибка", "Вы должны заполнить все поля!\n(исключением является только номер игрока)")
        
def button_table_2_click(Trick_name, Description, Main_performer):
    if Trick_name != "" and Description != "":
        connection = psycopg2.connect( host=host, user=user, password=password, database=db_name)
        cur = connection.cursor()
        cur.execute("INSERT INTO Best_tricks VALUES (%s, %s, %s)", (Trick_name, Description, Main_performer))
        connection.commit()
        cur.close()
        connection.close()
    else:
        messagebox.showinfo("Ошибка", "Вы должны заполнить все поля!\n(исключением является только номер игрока)")
        
def button_table_3_click(Player_id, Strength, Jumping,Endurance,Strategy, Technique, Speed):
    if Player_id != "":
        connection = psycopg2.connect( host=host, user=user, password=password, database=db_name)
        cur = connection.cursor()
        cur.execute("SELECT * FROM player_statistics WHERE Player_id = %s", (Player_id))
        flag = cur.fetchone()
        if flag is None:
            cur.execute("INSERT INTO player_statistics VALUES (%s, %s, %s, %s, %s, %s, %s)", (Player_id, Strength, Jumping,Endurance,Strategy, Technique, Speed))
        else:
            cur.execute("UPDATE player_statistics SET Strength = %s, Jumping = %s, Endurance = %s, Strategy = %s, Technique = %s, Speed = %s WHERE Player_id = %s;", (Strength, Jumping,Endurance,Strategy, Technique, Speed, Player_id))
        connection.commit()
        cur.close()
        connection.close()
    else:
        messagebox.showinfo("Ошибка", "Вы должны заполнить хотя бы id игрока!")

def button_table_4_click(competitions, enemy, Date, Result):
    if enemy != "" and competitions !="" and Date != "" and Result != "":
        connection = psycopg2.connect( host=host, user=user, password=password, database=db_name)
        cur = connection.cursor()
        cur.execute("INSERT INTO matches VALUES (%s, %s, %s, %s)", (competitions, enemy, Date, Result))
        connection.commit()
        cur.close()
        connection.close()
    else:
        messagebox.showinfo("Ошибка", "Вы должны заполнить все поля!")


def button_table_1_delete( id_e):
    if id_e != "":
        connection = psycopg2.connect( host=host, user=user, password=password, database=db_name)
        cur = connection.cursor()
        cur.execute("DELETE FROM members WHERE member_id = %s", (id_e))
        connection.commit()
        cur.close()
        connection.close()
        #Frame.id_e_d.delete(0, "END")
    else:
        messagebox.showinfo("Ошибка", "Вы должны ввести id!")

def button_table_2_delete(Trick_name):
    if Trick_name != "":
        connection = psycopg2.connect( host=host, user=user, password=password, database=db_name)
        cur = connection.cursor()
        cur.execute("DELETE FROM Best_tricks WHERE Trick_name = %s", [Trick_name])
        connection.commit()
        cur.close()
        connection.close()
        #Frame.id_e_d.delete(0, "END")
    else:
        messagebox.showinfo("Ошибка", "Вы должны ввести название приема!")
        
def button_table_3_delete(id_e):
    if id_e != "":
        connection = psycopg2.connect( host=host, user=user, password=password, database=db_name)
        cur = connection.cursor()
        cur.execute("DELETE FROM player_statistics WHERE Player_id = %s", (id_e))
        connection.commit()
        cur.close()
        connection.close()
        #Frame.id_e_d.delete(0, "END")
    else:
        messagebox.showinfo("Ошибка", "Вы должны ввести id!")
def button_matches_delete(id_e):
    if id_e != "":
        connection = psycopg2.connect( host=host, user=user, password=password, database=db_name)
        cur = connection.cursor()
        cur.execute("DELETE FROM matches WHERE enemy = %s", [id_e])
        connection.commit()
        cur.close()
        connection.close()
        #Frame.id_e_d.delete(0, "END")
    else:
        messagebox.showinfo("Ошибка", "Вы должны ввести id!")

def show_table(Frame):
    table = ttk.Treeview(Frame, columns=('Member_id', 'First_Name', 'Last_Name','Date_of_Birth','Height', 'Position', 'Number'), height=10, show='headings')
    table.heading('Member_id', text='Member_id')
    table.heading('First_Name', text='First_Name')
    table.heading('Last_Name', text='Last_Name')
    table.heading('Date_of_Birth', text='Date_of_Birth')
    table.heading('Height', text='Height')
    table.heading('Position', text='Position')
    table.heading('Number', text='Number')
    table.column('Member_id',width=70, anchor=tk.CENTER)
    table.column('First_Name',width=80, anchor=tk.CENTER)
    table.column('Last_Name',width=70, anchor=tk.CENTER)
    table.column('Date_of_Birth',width=100, anchor=tk.CENTER)
    table.column('Height',width=80, anchor=tk.CENTER)
    table.column('Position',width=180, anchor=tk.CENTER)
    table.column('Number',width=80, anchor=tk.CENTER)
    table.grid(column = 0, row = 5, sticky='N', columnspan=10, pady=15)
    connection = psycopg2.connect( host=host, user=user, password=password, database=db_name)
    cur = connection.cursor()
    cur.execute("SELECT * FROM members")
    [table.delete(i) for i in table.get_children()]
    [table.insert('', 'end', values=row) for row in cur.fetchall()]
    cur.close()
    connection.close()
    
def show_table2(Frame):
    table = ttk.Treeview(Frame, columns=('Trick_name', 'Description', 'Main_performer'), height=10, show='headings')
    table.heading('Trick_name', text='Trick_name')
    table.heading('Description', text='Description')
    table.heading('Main_performer', text='Main_performer')
    table.column('Trick_name',width=150, anchor=tk.CENTER)
    table.column('Description',width=540, anchor=tk.CENTER)
    table.column('Main_performer',width=100, anchor=tk.CENTER)
    table.grid(column = 0, row = 5, sticky='N', columnspan=5, pady=15)
    connection = psycopg2.connect( host=host, user=user, password=password, database=db_name)
    cur = connection.cursor()
    cur.execute("SELECT * FROM Best_tricks")
    [table.delete(i) for i in table.get_children()]
    [table.insert('', 'end', values=row) for row in cur.fetchall()]
    cur.close()
    connection.close()          
    
def show_table3(Frame):
    table = ttk.Treeview(Frame, columns=('Player_id', 'Strength', 'Jumping','Endurance','Strategy', 'Technique', 'Speed', 'irreplaceable'), height=10, show='headings')
    table.heading('Player_id', text='Player_id')
    table.heading('Strength', text='Strength')
    table.heading('Jumping', text='Jumping')
    table.heading('Endurance', text='Endurance')
    table.heading('Strategy', text='Strategy')
    table.heading('Technique', text='Technique')
    table.heading('Speed', text='Speed')
    table.heading('irreplaceable', text='irreplaceable')
    table.column('Player_id',width=70, anchor=tk.CENTER)
    table.column('Strength',width=80, anchor=tk.CENTER)
    table.column('Jumping',width=70, anchor=tk.CENTER)
    table.column('Endurance',width=100, anchor=tk.CENTER)
    table.column('Strategy',width=80, anchor=tk.CENTER)
    table.column('Technique',width=120, anchor=tk.CENTER)
    table.column('Speed',width=80, anchor=tk.CENTER)
    table.column('irreplaceable',width=150, anchor=tk.CENTER)
    table.grid(column = 0, row = 4, sticky='N', columnspan=10, pady=15)
    connection = psycopg2.connect( host=host, user=user, password=password, database=db_name)
    cur = connection.cursor()
    cur.execute("SELECT * FROM player_statistics")
    [table.delete(i) for i in table.get_children()]
    [table.insert('', 'end', values=row) for row in cur.fetchall()]
    cur.close()
    connection.close()   
    
def show_table4(Frame):
    table = ttk.Treeview(Frame, columns=('competitions_name', 'enemy', 'Date', 'Result'), height=8, show='headings')
    table.heading('competitions_name', text='competitions_name')
    table.heading('enemy', text='enemy')
    table.heading('Date', text='Date')
    table.heading('Result', text='Result')
    table.column('competitions_name',width=200, anchor=tk.CENTER)
    table.column('enemy',width=150, anchor=tk.CENTER)
    table.column('Date',width=100, anchor=tk.CENTER)
    table.column('Result',width=100, anchor=tk.CENTER)
    table.grid(column = 0, row = 5, sticky='N', columnspan=7, pady=15)
    connection = psycopg2.connect( host=host, user=user, password=password, database=db_name)
    cur = connection.cursor()
    cur.execute("SELECT * FROM matches")
    [table.delete(i) for i in table.get_children()]
    [table.insert('', 'end', values=row) for row in cur.fetchall()]
    cur.close()
    connection.close()
def show_matches(Frame, enemy_name):
    table = ttk.Treeview(Frame, columns=('competitions_name', 'enemy', 'Date', 'Result'), height=8, show='headings')
    table.heading('competitions_name', text='competitions_name')
    table.heading('enemy', text='enemy')
    table.heading('Date', text='Date')
    table.heading('Result', text='Result')
    table.column('competitions_name',width=200, anchor=tk.CENTER)
    table.column('enemy',width=150, anchor=tk.CENTER)
    table.column('Date',width=100, anchor=tk.CENTER)
    table.column('Result',width=100, anchor=tk.CENTER)
    table.grid(column = 0, row = 5, sticky='N', columnspan=7, pady=15)
    connection = psycopg2.connect( host=host, user=user, password=password, database=db_name)
    cur = connection.cursor()
    cur.execute("SELECT * FROM matches WHERE enemy = %s", [enemy_name])
    [table.delete(i) for i in table.get_children()]
    [table.insert('', 'end', values=row) for row in cur.fetchall()]
    cur.close()
    connection.close()   
def main():
    root = Tk()
    root.title("Haikyuu!!")
    root.iconbitmap("icon.ico")
    root.geometry("800x500+300+200")
    root.resizable(False, False)
    app = DB_menu()
    
    tab_control = ttk.Notebook(root)  
    tab1 = ttk.Frame(tab_control)
    tab2 = ttk.Frame(tab_control) 
    tab3 = ttk.Frame(tab_control) 
    tab4 = ttk.Frame(tab_control) 
    
    tab_control.add(tab1, text='Члены клуба') 
    tab_control.add(tab2, text='Лучшие приемы')
    tab_control.add(tab3, text='Статистика игрока') 
    tab_control.add(tab4, text='Матчи клуба') 
    ##################################################первая вкладка
    
    id_l = Label(tab1, text='id участника')  
    id_l.grid(column=0, row=0)
    #number_entry = tk.StringVar()
    id_e = Entry(tab1, width=3)
    id_e.grid(column=0, row=1)
    
    lbl1 = Label(tab1, text='Имя')  
    lbl1.grid(column=1, row=0)
    #name_entry = tk.StringVar()
    Name1 = Entry(tab1, width=30)
    Name1.grid(column=1, row=1)
    
    
    lbl2 = Label(tab1, text='Фамилия')  
    lbl2.grid(column=2, row=0)
    #name2_entry = tk.StringVar()
    Name2 = Entry(tab1, width=30)
    Name2.grid(column=2, row=1)
    lbl3 = Label(tab1, text='Дата рождения') 
     
    lbl3.grid(column=3, row=0)
    #dateb_entry = tk.StringVar()
    dateb_e = Entry(tab1, width=10)
    dateb_e.grid(column=3, row=1)  
    
    lbl4 = Label(tab1, text='Рост')  
    lbl4.grid(column=4, row=0)
    #height_entry = tk.StringVar()
    height_e = Entry(tab1, width=3)
    height_e.grid(column=4, row=1)
    
    lbl5 = Label(tab1, text='Позиция')  
    lbl5.grid(column=5, row=0)
    #Position_entry = tk.StringVar()
    Position_e = Entry(tab1, width=30)
    Position_e.grid(column=5, row=1)  
    
    lbl6 = Label(tab1, text='Номер')  
    lbl6.grid(column=6, row=0)
    #number_entry = tk.StringVar()
    number_e = Entry(tab1, width=2)
    number_e.grid(column=6, row=1)
    
    btn_add = Button(tab1, text="Добавить участника",width=15, height=1, background="#555", foreground="#ccc",
             padx="10", pady="4", font=("Verdana", 9, "bold"), command=lambda: [button_table_1_click(id_e.get(), Name1.get(), Name2.get(), dateb_e.get(),height_e.get(), Position_e.get(), number_e.get()), show_table(tab1)])
    btn_add.grid(column=2, row=2, pady=15)
    separator = ttk.Separator(tab1, orient='horizontal')
    separator.grid(row=3, column=0, columnspan=99, sticky=(tk.W, tk.E), pady=5)
    
    Delete_lbl = Label(tab1, text='Введите id участника,\nчтобы удалить его из таблицы:')
    Delete_lbl.grid(column=1, row=4) 
    id_e_d = Entry(tab1, width=3)
    id_e_d.grid(column=2, row=4)
    btn_delete = Button(tab1,text="Удалить участника",width=15, height=2, background="#555", foreground="#ccc",
             padx="10", pady="4", font=("Verdana", 8, "bold"), command=lambda: [button_table_1_delete(id_e_d.get()), show_table(tab1)])
    btn_delete.place(x=400, y=115)
    app = show_table(tab1)
    btn_show = Button(tab1,text="Обновить таблицу",width=15, height=2, background="#555", foreground="#ccc",
             padx="10", pady="4", font=("Verdana", 8, "bold"), command=lambda: show_table(tab1))
    btn_show.grid(column=5, row=6)
    
    ##################################################вторая вкладка
    trik_name_lbl = Label(tab2, text='Название приема')  
    trik_name_lbl.grid(column=0, row=0)
    trik_e = Entry(tab2, width=30)
    trik_e.grid(column=0, row=1)
      
    dcrptn_lbl = Label(tab2, text='Описание')  
    dcrptn_lbl.grid(column=1, row=0)
    dcrptn_e = Entry(tab2, width=80)
    dcrptn_e.grid(column=1, row=1)
    
    performer_lbl = Label(tab2, text='Исполнитель')  
    performer_lbl.grid(column=2, row=0)
    performer_e = Entry(tab2, width=3)
    performer_e.grid(column=2, row=1)
    
    btn_add = Button(tab2, text="Добавить прием",width=15, height=1, background="#555", foreground="#ccc",
             padx="10", pady="4", font=("Verdana", 9, "bold"), command=lambda: [button_table_2_click(trik_e.get(), dcrptn_e.get(), performer_e.get()), show_table2(tab2)])
    btn_add.grid(column=1, row=2, pady=15)
    separator = ttk.Separator(tab2, orient='horizontal')
    separator.grid(row=3, column=0, columnspan=4, sticky=(tk.W, tk.E))
    
    Delete_lbl = Label(tab2, text='Введите название приема,\nчтобы удалить его из таблицы:')
    Delete_lbl.grid(column=0, row=4) 
    id_e_d2 = Entry(tab2, width=30)
    id_e_d2.place(x=190, y=115)
    btn_delete = Button(tab2,text="Удалить прием",width=15, height=1, background="#555", foreground="#ccc",
             padx="10", pady="4", font=("Verdana", 8, "bold"), command=lambda: [button_table_2_delete(id_e_d2.get()), show_table2(tab2)])
    btn_delete.grid(column = 1, row = 4, sticky='N', columnspan=2, pady=7) 
    app = show_table2(tab2)
    btn_show = Button(tab2,text="Обновить таблицу",width=15, height=2, background="#555", foreground="#ccc",
             padx="10", pady="4", font=("Verdana", 8, "bold"), command=lambda: show_table2(tab2))
    btn_show.grid(column=0, row=6)
    ##################################################третья вкладка
    Player_id_lbl = Label(tab3, text='id игрока')  
    Player_id_lbl.grid(column=0, row=0)
    Player_id_e = Entry(tab3, width=4)
    Player_id_e.grid(column=0, row=1)
    
    Strength_lbl = Label(tab3, text='Сила')  
    Strength_lbl.grid(column=1, row=0)  
    Strength_e = Entry(tab3, width=4)
    Strength_e.grid(column=1, row=1)
    
    Jumping_lbl = Label(tab3, text='Прыжки')  
    Jumping_lbl.grid(column=2, row=0)
    Jumping_e = Entry(tab3, width=4)
    Jumping_e.grid(column=2, row=1)
    
    Endurance_lbl = Label(tab3, text='Выносливость')  
    Endurance_lbl.grid(column=3, row=0)
    Endurance_e = Entry(tab3, width=4)
    Endurance_e.grid(column=3, row=1)
      
    Strategy_lbl = Label(tab3, text='Стратегия')  
    Strategy_lbl.grid(column=4, row=0)
    Strategy_e = Entry(tab3, width=4)
    Strategy_e.grid(column=4, row=1)
    
    Technique_lbl = Label(tab3, text='Техника')  
    Technique_lbl.grid(column=5, row=0)
    Technique_e = Entry(tab3, width=4)
    Technique_e.grid(column=5, row=1)
      
    Speed_lbl = Label(tab3, text='Скорость')  
    Speed_lbl.grid(column=6, row=0)
    Speed_e = Entry(tab3, width=4)
    Speed_e.grid(column=6, row=1)
    
    # Speed_lbl = Label(tab3, text='Незаменимость')  
    # Speed_lbl.grid(column=7, row=0)
    # Speed_e = Entry(tab3, width=4)
    # Speed_e.grid(column=7, row=1)
    
    btn_add3 = Button(tab3, text="Добавить или изменить статистику",width=30, height=1, background="#555", foreground="#ccc",
             padx="10", pady="4", font=("Verdana", 9, "bold"), command=lambda: [button_table_3_click(Player_id_e.get(), Strength_e.get(), Jumping_e.get(), Endurance_e.get(),Strategy_e.get(), Technique_e.get(), Speed_e.get()), show_table3(tab3)])
    btn_add3.grid(column=0, row=2,  sticky='N', columnspan=6, pady=15)
    separator = ttk.Separator(tab3, orient='horizontal')
    separator.grid(row=3, column=0, columnspan=99, sticky=(tk.W, tk.E), pady=5)
    separator = ttk.Separator(tab3, orient='vertical')
    separator.grid(row=0, column=7,rowspan=3, sticky='ns')
    
    Delete_lbl = Label(tab3, text='Введите id участника,чтобы \nудалить его статистику из таблицы:')
    Delete_lbl.grid(column=8, row=1) 
    id_e_d3 = Entry(tab3, width=3)
    id_e_d3.grid(column=9, row=1, pady=15)
    btn_delete = Button(tab3,text="Удалить статистику",width=15, height=2, background="#555", foreground="#ccc",
             padx="10", pady="4", font=("Verdana", 8, "bold"), command=lambda: [button_table_3_delete(id_e_d3.get()), show_table3(tab3)])
    btn_delete.grid(column=9, row=2)
    app = show_table3(tab3)
    btn_show = Button(tab3,text="Обновить таблицу",width=15, height=2, background="#555", foreground="#ccc",
             padx="10", pady="4", font=("Verdana", 8, "bold"), command=lambda: show_table3(tab3))
    btn_show.grid(column=9, row=5)
    ##################################################третья вкладка
   
    competitions_name_lbl = Label(tab4, text='Название турнира')  
    competitions_name_lbl.grid(column=1, row=0)
    competitions_e = Entry(tab4, width=30)
    competitions_e.grid(column=1, row=1)
      
    enemy_lbl = Label(tab4, text='Соперник')  
    enemy_lbl.grid(column=2, row=0)
    enemy_e = Entry(tab4, width=30)
    enemy_e.grid(column=2, row=1)
    
    Date_lbl = Label(tab4, text='Дата матча')  
    Date_lbl.grid(column=3, row=0)
    Date_e = Entry(tab4, width=10)
    Date_e.grid(column=3, row=1)
      
    Result_lbl = Label(tab4, text='Результат')  
    Result_lbl.grid(column=4, row=0)
    Result_e = Entry(tab4, width=10)
    Result_e.grid(column=4, row=1)
    
    btn_add4 = Button(tab4, text="Добавить матч",width=30, height=1, background="#555", foreground="#ccc",
             padx="10", pady="4", font=("Verdana", 9, "bold"), command=lambda: [button_table_4_click(competitions_e.get(), enemy_e.get(), Date_e.get(), Result_e.get()), show_table4(tab4)])
    btn_add4.grid(column=0, row=2,  sticky='N', columnspan=4, pady=15)
    separator = ttk.Separator(tab4, orient='horizontal')
    separator.grid(row=4, column=0, columnspan=99, sticky=(tk.W, tk.E), pady=10)
    separator = ttk.Separator(tab4, orient='vertical')
    separator.grid(row=0, column=5,rowspan=4, sticky='ns')
    
    Delete_lbl = Label(tab4, text='Введите название команды-соперника:')
    Delete_lbl.grid(column=6, row=0) 
    id_e_d4 = Entry(tab4, width=25)
    id_e_d4.grid(column=6, row=1, pady=15)
    btn_show_m = Button(tab4,text="Показать все матчи с этой командой",width=30, height=1, background="#555", foreground="#ccc",
             padx="10", pady="4", font=("Verdana", 6, "bold"), command=lambda: show_matches(tab4, id_e_d4.get()))
    btn_show_m.grid(column=6, row=2)
    btn_delete = Button(tab4,text="Удалить все матчи с этой командой",width=30, height=1, background="#555", foreground="#ccc",
             padx="10", pady="4", font=("Verdana", 6, "bold"), command=lambda: [button_matches_delete(id_e_d4.get()), show_table4(tab4)])
    btn_delete.grid(column=6, row=3)
    app = show_table4(tab4)
    btn_show = Button(tab4,text="Обновить таблицу",width=15, height=2, background="#555", foreground="#ccc",
             padx="10", pady="4", font=("Verdana", 8, "bold"), command=lambda: show_table4(tab4))
    btn_show.grid(column=6, row=6)
    
    
    
    ###########################################
    tab_control.grid(column=0, row=0, sticky='NS')
    
    # cur.close()
    # connection.close()
    root.mainloop()
 
 
if __name__ == '__main__':
    main()