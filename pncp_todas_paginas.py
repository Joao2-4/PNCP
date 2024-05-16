import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from PIL import Image, ImageTk
import json
import requests
from datetime import datetime

def pncp():
    esfera = esfera_combobox.get()
    uf_sigla = uf_combobox.get()
    data_inicial = data_inicial_entry.get()
    data_final = data_final_entry.get()

    # Verifica se os campos foram preenchidos
    if not esfera or not uf_sigla or not data_inicial or not data_final:
        messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
        return

    # Verifica se a esfera selecionada é válida
    if esfera not in ["E", "M"]:
        messagebox.showerror("Erro", "Por favor, selecione uma esfera válida.")
        return

    # Verifica se as datas estão no formato correto
    if not validar_data(data_inicial) or not validar_data(data_final):
        messagebox.showerror("Erro", "Por favor, insira datas válidas no formato AAAAMMDD.")
        return

    # Verifica se as datas estão dentro do intervalo permitido
    if not verificar_intervalo_de_datas(data_inicial, data_final):
        messagebox.showerror("Erro", "Por favor, insira datas dentro do intervalo permitido.")
        return

    url = 'https://pncp.gov.br/api/consulta/v1/contratos'
    headers = {'accept': '*/*'}
    todos_os_registros = []

    for pagina in range(1, 11):  # Consulta até a décima página
        params = {
            'dataInicial': data_inicial,
            'dataFinal': data_final,
            'pagina': str(pagina)
        }

        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            dados = response.json()
            todos_os_registros.extend(dados['data'])
        else:
            messagebox.showerror("Erro", f"Erro ao consultar a API: {response.status_code}")
            return

    registros_filtrados = [item for item in todos_os_registros if item['orgaoEntidade']['esferaId'] == esfera and item['unidadeOrgao']['ufSigla'] == uf_sigla]

    # Abre uma caixa de diálogo para selecionar o local e o nome do arquivo
    file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("Arquivos JSON", "*.json")])
    
    if not file_path:
        messagebox.showerror("Erro", "Nenhum arquivo selecionado.")
        return
    
    with open(file_path, "w") as file:
        json.dump(registros_filtrados, file, indent=4)
    
    messagebox.showinfo("Sucesso", f"Total de registros para a esfera '{esfera}' e UF '{uf_sigla}': {len(registros_filtrados)}\nDados filtrados salvos em: {file_path}")

def validar_data(data):
    try:
        datetime.strptime(data, "%Y%m%d")
        return True
    except ValueError:
        return False

def verificar_intervalo_de_datas(data_inicial, data_final):
    data_atual = datetime.now()
    ano_atual = data_atual.year
    mes_atual = data_atual.month

    data_inicial_dt = datetime.strptime(data_inicial, "%Y%m%d")
    data_final_dt = datetime.strptime(data_final, "%Y%m%d")

    # Verifica se o ano está dentro do intervalo permitido
    if not 2000 <= data_inicial_dt.year <= ano_atual or not 2000 <= data_final_dt.year <= ano_atual:
        return False

    # Verifica o mês máximo permitido para o ano atual
    if data_inicial_dt.year == ano_atual and data_inicial_dt.month > mes_atual:
        return False

    return True

# Criando a janela principal
root = tk.Tk()
root.title("PNCP")
root.configure(bg="black")  # Cor de fundo preta

# Ícone da janela
root.iconbitmap("icon.ico")

# Criando os widgets
esfera_label = tk.Label(root, text="Esfera:", font=("Verdana", 12), bg="black", fg="white")
esfera_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")

esferas = ["E", "M"]
esfera_combobox = ttk.Combobox(root, values=esferas, font=("Verdana", 12), state="readonly")
esfera_combobox.grid(row=1, column=1, padx=5, pady=5)

uf_label = tk.Label(root, text="UF Sigla:", font=("Verdana", 12), bg="black", fg="white")
uf_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")

# Lista de estados do Brasil
estados_brasil = [
    "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG",
    "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"
]
uf_combobox = ttk.Combobox(root, values=estados_brasil, font=("Verdana", 12), state="readonly")
uf_combobox.grid(row=2, column=1, padx=5, pady=5)

data_inicial_label = tk.Label(root, text="Data Inicial (AAAAMMDD):", font=("Verdana", 12), bg="black", fg="white")
data_inicial_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")
data_inicial_entry = tk.Entry(root, font=("Verdana", 12))
data_inicial_entry.grid(row=3, column=1, padx=5, pady=5)

data_final_label = tk.Label(root, text="Data Final (AAAAMMDD):", font=("Verdana", 12), bg="black", fg="white")
data_final_label.grid(row=4, column=0, padx=5, pady=5, sticky="e")
data_final_entry = tk.Entry(root, font=("Verdana", 12))
data_final_entry.grid(row=4, column=1, padx=5, pady=5)

filtrar_button = tk.Button(root, text="Filtrar e Salvar", font=("Verdana", 14, "bold"), bg="#0D2649", fg="white", command=pncp, bd=0, relief=tk.RIDGE)
filtrar_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="we")

# Iniciando o loop principal da interface
root.mainloop()
