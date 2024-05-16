import requests
import json
from tkinter import filedialog

def consulta_api(data_inicial, data_final, pagina, cnpj_orgao=None, codigo_unidade_administrativa=None, usuario_id=None, tamanho_pagina=None):
    # Faz a solicitação à API
    url = 'https://pncp.gov.br/api/consulta/v1/contratos'
    params = {
        'dataInicial': data_inicial,
        'dataFinal': data_final,
        'pagina': pagina
    }
    # Adiciona parâmetros opcionais se fornecidos
    if cnpj_orgao:
        params['cnpjOrgao'] = cnpj_orgao
    if codigo_unidade_administrativa:
        params['codigoUnidadeAdministrativa'] = codigo_unidade_administrativa
    if usuario_id:
        params['usuarioId'] = usuario_id
    if tamanho_pagina:
        params['tamanhoPagina'] = tamanho_pagina
    
    headers = {
        'accept': '*/*'
    }

    response = requests.get(url, params=params, headers=headers)

    # Verifica se a solicitação foi bem-sucedida
    if response.status_code == 200:
        # Retorna os dados obtidos da API
        return response.json()
    else:
        print("Erro ao fazer a solicitação à API:", response.status_code)
        return None

def salvar_dados(data):
    # Abre uma caixa de diálogo para selecionar o local e o nome do arquivo
    file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("Arquivos JSON", "*.json")])
    
    if not file_path:
        print("Nenhum arquivo selecionado.")
        return
    
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)
    
    print("Dados salvos com sucesso em:", file_path)

def carrega():
    # Solicita entrada do usuário para os parâmetros da consulta
    data_inicial = input("Digite a data inicial (formato YYYYMMDD): ")
    data_final = input("Digite a data final (formato YYYYMMDD): ")
    pagina = input("Digite o número da página: ")
    cnpj_orgao = input("Digite o CNPJ do órgão (opcional): ")
    codigo_unidade_administrativa = input("Digite o código da unidade administrativa (opcional): ")
    usuario_id = input("Digite o ID do usuário (opcional): ")
    tamanho_pagina = input("Digite o tamanho da página (opcional): ")

    # Consulta a API para obter os dados
    data = consulta_api(data_inicial, data_final, pagina, cnpj_orgao, codigo_unidade_administrativa, usuario_id, tamanho_pagina)

    if data:
        # Extrair informações adicionais
        total_registros = data['totalRegistros']
        total_paginas = data['totalPaginas']
        numero_pagina = data['numeroPagina']
        paginas_restantes = data['paginasRestantes']
        empty = data['empty']

        print("Informações adicionais:")
        print(f"Total de registros: {total_registros}")
        print(f"Total de páginas: {total_paginas}")
        print(f"Número da página atual: {numero_pagina}")
        print(f"Páginas restantes: {paginas_restantes}")

        print(f"Está vazio? {empty}")
        # Lista para armazenar as esferas fornecidas pelo usuário
        listEsfera = []

        # Solicita ao usuário que insira o ID da esfera até que o valor 0 seja inserido
        for _ in range(4):
            esfera_id = input("Digite o ID da esfera: ")
            esferaupper = esfera_id.upper()
            if esfera_id == "0":  
                break
            listEsfera.append(esferaupper)

        print(listEsfera)

        uf_sigla = input("Digite o Estado que deseja: ")
        filtered_data = [item for item in data['data'] if item['orgaoEntidade']['esferaId'] in listEsfera and item['unidadeOrgao']['ufSigla'] == uf_sigla]

        # Contar o número de registros correspondentes
        total_registros_filtrados = len(filtered_data)
        print(f"Total de registros para a esfera '{listEsfera}' e UF '{uf_sigla}': {total_registros_filtrados}")

        # Salvar os dados filtrados em um novo arquivo JSON
        salvar_dados(filtered_data)

# Chama a função para carregar e processar os dados
carrega()
