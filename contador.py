import tkinter as tk
from tkinter import ttk
import mysql.connector

materias = ['Banco de Dados Relacional',
            'Estrutura de Dados',
            'Engenharia de Dados',
            'Desenvolvimento Web II',
            'Técnicas de Programação',
            'Matemática para programação']

faltas_por_materia = {materia: 0 for materia in materias}

# Função para salvar as faltas no banco de dados MySQL
def salvar_faltas(materia, faltas):
    # Estabelecer conexão com o banco de dados MySQL
    conexao = mysql.connector.connect(
        host="localhost",
        user="root",
        password="fatec23",
        database="contador_faltas"
    )

    # Criar cursor para executar as consultas
    cursor = conexao.cursor()

    # Inserir ou atualizar as faltas no banco de dados
    consulta = "INSERT INTO materia_falt (idcurso, nomecursos, faltas) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE faltas = %s"
    valores = (materias.index(materia) + 1, materia, faltas, faltas)
    cursor.execute(consulta, valores)

    # Commit para salvar as alterações no banco de dados
    conexao.commit()

    # Fechar cursor e conexão com o banco de dados
    cursor.close()
    conexao.close()

# Função para carregar as faltas do banco de dados MySQL
def carregar_faltas():
    # Estabelecer conexão com o banco de dados MySQL
    conexao = mysql.connector.connect(
        host="localhost",
        user="root",
        password="fatec23",
        database="contador_faltas"
    )

    # Criar cursor para executar as consultas
    cursor = conexao.cursor()

    # Consultar as faltas no banco de dados
    consulta = "SELECT nomecursos, faltas FROM materia_falt"
    cursor.execute(consulta)

    # Recuperar os dados e atualizar o dicionário de faltas
    for materia, quantidade in cursor:
        faltas_por_materia[materia] = quantidade

    # Fechar cursor e conexão com o banco de dados
    cursor.close()
    conexao.close()

# Função para adicionar faltas
def adicionar_faltas(materia):
    falta = int(faltas_entry.get())
    faltas_por_materia[materia] += falta

    salvar_faltas(materia, faltas_por_materia[materia])  # Salvar as faltas no banco de dados

    faltas_atual_label.config(text=f'Número de faltas atual: {faltas_por_materia[materia]}')

    aviso = verificar_aviso(materia)
    aviso_label.config(text=aviso)
    faltas_entry.delete(0, tk.END)

def verificar_aviso(materia):
    limite_faltas = 20
    total_faltas = faltas_por_materia[materia]

    if total_faltas >= limite_faltas:
        return f'AVISO: Você já tem {total_faltas} faltas em {materia}. Considere seu limite de faltas!'
    else:
        return ""

# Criar janela principal
janela = tk.Tk()
janela.title("Contador de Faltas")
janela.geometry("1000x500")  # Definindo a geometria da janela

# Carregar as faltas do banco de dados ao iniciar o programa
carregar_faltas()

# Criar frame principal
frame_principal = tk.Frame(janela)
frame_principal.pack(expand=True)

# Criar componentes da interface
materia_label = tk.Label(frame_principal, text="Escolha a matéria:")
materia_label.pack(pady=10)

materia_var = tk.StringVar()
materia_combobox = ttk.Combobox(frame_principal, textvariable=materia_var, state="readonly", width=30)
materia_combobox['values'] = tuple(materias)
materia_combobox.pack(pady=5)

faltas_label = tk.Label(frame_principal, text="Adicione o número de faltas:")
faltas_label.pack()

faltas_entry = tk.Entry(frame_principal, width=30)
faltas_entry.pack(pady=5)

adicionar_faltas_button = tk.Button(frame_principal, text="Adicionar Faltas", command=lambda: adicionar_faltas(materia_combobox.get()), width=30)
adicionar_faltas_button.pack(pady=10)

faltas_atual_label = tk.Label(frame_principal, text="Número de faltas atual:", width=30)
faltas_atual_label.pack()

aviso_label = tk.Label(frame_principal, text="", width=30)
aviso_label.pack(pady=10)

# Centralizar os componentes verticalmente
frame_principal.pack(expand=True, pady=100)

# Iniciar loop da interface gráfica
janela.mainloop()
