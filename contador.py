import tkinter as tk
from tkinter import ttk

materias = ['Banco de Dados Relacional',
            'Estrutura de Dados',
            'Engenharia de Dados',
            'Desenvolvimento Web II',
            'Técnicas de Programação',
            'Matemática para programação']

faltas_por_materia = {materia: 0 for materia in materias}

def adicionar_faltas(materia):
    falta = int(faltas_entry.get())
    faltas_por_materia[materia] += falta
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

# Criar frame principal
frame_principal = tk.Frame(janela)
frame_principal.pack(expand=True)

# Criar componentes da interface
boas_vindas = tk.Label(frame_principal, text='Bem vindo(a) ao meu', font=('Arial',10))
nome_materia_label = tk.Label(frame_principal, text="Contador de faltas", font=('Arial',20))
nome_materia_label.pack(pady=10)


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
