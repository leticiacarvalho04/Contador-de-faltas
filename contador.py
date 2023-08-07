import mysql.connector
import tkinter as tk
from tkinter import ttk

modo_atual = 'dark'

def bg():
    light_icon = tk.PhotoImage(file='brightness.png')
    dark_icon = tk.PhotoImage(file='dark.png')

    dark_mode_button = tk.Button(root, command=toggle_dark_mode)
    dark_mode_button.config(image=dark_icon, bd=0, bg='#1d1d1d')
    dark_mode_button.pack(pady=10)

    canvas = tk.Canvas(root, width=600, height=20, bg='#1d1d1d', bd=0, highlightthickness=0, relief='ridge')
    canvas.pack()

def toggle_dark_mode():
    global modo_atual

    if modo_atual == 'dark':
        apply_light_mode()  # Apply light mode settings
        root['bg'] = 'white'
        dark_mode_button.config(image=light_icon, bg='white')
        modo_atual = 'light'
    else:
        apply_dark_mode()  # Apply dark mode settings
        root['bg'] = '#1d1d1d'
        dark_mode_button.config(image=dark_icon, bg='#1d1d1d')
        modo_atual = 'dark'

def apply_light_mode():
    style.configure("TLabel", background="lightgray", foreground="black", font=("Arial", 12))
    style.configure("TButton", background="blue", foreground="black", font=("Arial", 12))
    style.configure("Dark.Treeview.Heading", background="#1d1d1d", foreground="black")
    style.configure("Dark.Treeview", background="#1d1d1d", foreground="black", rowheight=25)

def apply_dark_mode():
    style.configure("TLabel", background="#1d1d1d", foreground="white", font=("Arial", 12))
    style.configure("TButton", background="gray", foreground="white", font=("Arial", 12))
    style.configure("Dark.Treeview.Heading", background="#1d1d1d", foreground="white")
    style.configure("Dark.Treeview", background="#1d1d1d", foreground="white", rowheight=25)

def create_database_table():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="fatec23",
    )
    cur = connection.cursor()
    
    cur.execute("CREATE DATABASE IF NOT EXISTS contador")
    cur.execute("USE contador")
    cur.execute('''
        CREATE TABLE IF NOT EXISTS materia_falta (
            codigo INT AUTO_INCREMENT PRIMARY KEY,
            materia VARCHAR(60),
            falta INT NOT NULL
        )
    ''')
    
    connection.commit()
    cur.close()
    connection.close()

def materias():
    materia = combo_box_1.get()
    faltas = int(entry_faltas.get())  # Convert the value to an integer

    connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="fatec23",
                database="contador"
            )
    cur = connection.cursor()
    
    # Verificar se a matéria já existe no banco de dados
    query_select = "SELECT falta FROM materia_falta WHERE materia = %s"
    cur.execute(query_select, (materia,))
    result = cur.fetchone()

    if result:  # Se a matéria já existe, atualize o número de faltas
        faltas += int(result[0])  # Converta o valor recuperado em um número inteiro e adicione
        query_update = "UPDATE materia_falta SET falta = %s WHERE materia = %s"
        cur.execute(query_update, (faltas, materia))
    else:  # Se a matéria não existe, insira uma nova entrada
        query_insert = "INSERT INTO materia_falta (materia, falta) VALUES (%s, %s)"
        cur.execute(query_insert, (materia, faltas))

    connection.commit()

    cur.close()
    connection.close()

    # Após inserir os dados, atualize a tabela
    update_table()

def clear_materia():
    materia = combo_box_1.get()

    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="fatec23",
        database="contador"
    )
    cur = connection.cursor()

    query = "DELETE FROM materia_falta WHERE materia = %s"
    cur.execute(query, (materia,))

    connection.commit()

    cur.close()
    connection.close()

    update_table()


def update_table():
    connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="fatec23",
                database="contador"
            )
    cur = connection.cursor()

    cur.execute("SELECT materia, falta FROM materia_falta")
    data = cur.fetchall()

    # Limpar a tabela antes de atualizá-la
    for row in table.get_children():
        table.delete(row)

    # Atualizar a tabela com os dados obtidos do banco de dados
    for item in data:
        table.insert("", "end", values=item)

    cur.close()
    connection.close()

root = tk.Tk()
root.title("Attendance Tracker")
root.geometry("600x600")

# Styles
style = ttk.Style()
style.configure("TLabel", background="lightgray", font=("Arial", 12))
style.configure("TButton", background="blue", foreground="white", font=("Arial", 12))

# Create the toggle dark mode button
light_icon = tk.PhotoImage(file='brightness.png')
dark_icon = tk.PhotoImage(file='dark.png')
dark_mode_button = tk.Button(root, command=toggle_dark_mode, bd=0, bg='#1d1d1d')
dark_mode_button.config(image=dark_icon)
dark_mode_button.pack(pady=10)

#Seleção das matérias
combo_box_1 = tk.StringVar(root)
combo_box_1.set("Matérias")
options_1 = ["Banco de Dados – Relacional", "Engenharia de Software II", "Estrutura de Dados", 'Desenvolvimento Web II','Técnicas de Programação',
             'Matemática para Computação']
option_menu_1 = tk.OptionMenu(root, combo_box_1, *options_1)
option_menu_1.config()
option_menu_1.pack(pady=10)

entry_faltas = tk.Entry(root)
entry_faltas.pack(padx=10)

filter_button = tk.Button(root, text="Registrar faltas", command=materias)
filter_button.pack(pady=10)

# Create the table
table = ttk.Treeview(root, columns=("Matérias", "Faltas"), show="headings")
table.heading("Matérias", text="Matérias")
table.heading("Faltas", text="Faltas")
table.pack()

style.configure("Dark.Treeview.Heading", background="#1d1d1d", foreground="white")
style.configure("Dark.Treeview", background="#1d1d1d", foreground="white", rowheight=25)

# Update the table initially
create_database_table()
update_table()

btn_clear = tk.Button(root, text='Limpar faltas', command=clear_materia)
btn_clear.pack(pady=10)

root.mainloop()
