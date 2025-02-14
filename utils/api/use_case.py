from ..connection_erp.use_case import push_maxi
from csv import writer
import pandas as pd
from dotenv import load_dotenv
import os

# config dotenv
load_dotenv()
__TOKEN = os.getenv("TOKEN")

def update_data_Empresas(urlItem, csv_name):
    #Atualiza data frame de empresas

    print('Gerando Arquivo de Empresas...')

    data = push_maxi(__TOKEN, 1,urlItem)
    total_paginas = data['QuantidadeDePaginas']
    
    with open(csv_name, 'w', newline='') as datas:
        writer_object = writer(datas)
        writer_object.writerow(["EMPRESA_ID;RAZAO_SOCIAL;CPF_CNPJ;EMAIL;APELIDO"])
        for pagina in range(total_paginas):
            pagina += 1
            data = push_maxi(__TOKEN,pagina, urlItem)
            for item in data['Registros']:
                writer_object = writer(datas)
                razao_social = str(item["Razao_social"])

                razao_social = razao_social.replace(',', '')
                razao_social = razao_social.replace(';', '')
                razao_social = razao_social.replace('\n', '')
                
                writer_object.writerow([f'{item["Empresa_Id"]};{razao_social};{str(item["CNPJ_CPF"])};{str(item["Email"])};{item["Apelido"]}'])  

    datas.close() 

def update_data_Itens(urlItem, csv_name):

    print('Gerando Arquivo de Itens...')
    data = push_maxi(__TOKEN, 1,urlItem)
    total_paginas = data['QuantidadeDePaginas']
    
    with open(csv_name, 'w', newline='') as datas:
        writer_object = writer(datas)
        writer_object.writerow(["ID_ITEM;CODIGO;EMPRESA;ID_GRUPO;UNIDADE_DE_MEDIDA"])
        for pagina in range(total_paginas):
            pagina += 1
            data = push_maxi(__TOKEN,pagina, urlItem)
            for item in data['Registros']:  
                writer_object = writer(datas)
                writer_object.writerow([f'{item["Item_Id"]};{item["Codigo"]};HPC;{item["Grupo_Id"]};{item["Unidade_principal"]}'])  
        datas.close()

def update_data_Estoque(urlEstoque, csv_name):

    print('Gerando Arquivo de Estoque...')
    df_empresas = pd.read_csv('./files/Empresas_Maxi.csv', encoding='latin-1', sep = ';',  on_bad_lines='skip')
    data = push_maxi(__TOKEN, 1,urlEstoque)
    total_paginas = data['QuantidadeDePaginas']
    
    with open(csv_name, 'w', newline='') as datas:
        writer_object = writer(datas)
        writer_object.writerow(["ID_ITEM;TIPO_PRODUTO;EMPRESA;ESTOQUE;ENDERECO_ESTOQUE"])

        for pagina in range(total_paginas):
            pagina += 1
            data = push_maxi(__TOKEN, pagina, urlEstoque)
            for item in data['Registros']:
                if item["Estoque"] == "Matéria-prima" and item["EnderecoEstoque_codigo"] != None and item["EnderecoEstoque_descricao"] != "SIMILAR": 
                    writer_object = writer(datas)

                    empresa_estoque = df_empresas.loc[df_empresas['EMPRESA_ID'] == str(item["Propria_empresa_Id"]), 'APELIDO']
                    empresa_estoque = empresa_estoque.tolist()
                    empresa_estoque = empresa_estoque[0]

                    writer_object.writerow([f'{item["Item_Id"]};{item["Estoque"]};{empresa_estoque};{item["Quantidade"]};{item["EnderecoEstoque_codigo"]}'])

        datas.close()

def analyze_data():
    print('Analisando Dados...')
    itens_lista = []

    df_estoque = pd.read_csv('./files/Itens_Estoque.csv', encoding='latin-1', sep=';')
    df_itens = pd.read_csv('./files/Itens_Maxi.csv', encoding='latin-1', sep=';')

    df_estoque_agrupado = df_estoque.groupby('ID_ITEM')['ESTOQUE'].sum().reset_index()
    print(df_estoque_agrupado.head())

    for i in df_estoque_agrupado.index:
        id_item_estoque = df_estoque_agrupado['ID_ITEM'][i]
        quantidade_em_estoque = df_estoque_agrupado['ESTOQUE'][i]
        quantidade_em_estoque = int(round(quantidade_em_estoque, 2))

        # Procura o código correspondente
        codigo_series = df_itens.loc[df_itens['ID_ITEM'] == id_item_estoque, 'CODIGO']
        codigo_list = codigo_series.to_list()

        if not codigo_list:
            # Se não encontrar nenhum código, exibe uma mensagem e pula para o próximo item.
            print(f"ID_ITEM {id_item_estoque} não encontrado em df_itens.")
            continue

        codigo = codigo_list[0]
        codigo = codigo.replace('-HP', '')

        if codigo == 'RB250':
            pass  # ou continue, se você quiser pular esse item
        else:
            if codigo == '387TC-32':
                print(codigo, quantidade_em_estoque)
            item_add = [id_item_estoque, codigo, quantidade_em_estoque]
            itens_lista.append(item_add)

    return itens_lista


def analyze_document():

    print('Analisando Arquivo...')

    df_estoque = pd.read_csv('./estoque_temporario/Estoque - HPC.csv', sep = ';')
    df_mangueiras = pd.read_excel('./estoque_temporario/Planilha_Modelo_Inventario_MAXIPROD - GUSTAVO.xlsx')
    df_estoque_ghp_serra = pd.read_csv('./estoque_temporario/Estoque - SERRA.csv', sep = ';')
    
    df_estoque = df_estoque.loc[df_estoque['Estoque']=='Matéria-prima']
    df_estoque = df_estoque.dropna(subset=['Endereço de estoque'])
    df_estoque = df_estoque[df_estoque['Grupo'] != 3.1].reset_index()

    df_estoque_ghp_serra = df_estoque_ghp_serra.loc[df_estoque_ghp_serra['Estoque']=='Matéria-prima']
    df_estoque_ghp_serra = df_estoque_ghp_serra.dropna(subset=['Endereço de estoque'])

    codigos = []
    quantidades = []

    df_mangueiras = df_mangueiras.dropna(subset=['Quantidade contada (metros)'])
    df_mangueiras = df_mangueiras[df_mangueiras['Quantidade contada (metros)'] != 'SEM CONTAGEM'].reset_index()

    for i in df_estoque_ghp_serra.index:

        codigo = df_estoque_ghp_serra['Item'][i]
        quantidade = df_estoque_ghp_serra['Quantidade'][i]
        quantidade_nr = df_estoque_ghp_serra['Qt não reservada'][i]

        flag = pd.isna(quantidade_nr)

        if flag != True:
            quantidade = quantidade_nr

        quantidade = quantidade.replace('.', '_')
        quantidade = quantidade.replace(',', '.')
        quantidade = quantidade.replace('_', '')

        quantidade = float(quantidade)

        codigos.append(codigo)
        quantidades.append(quantidade)

    for i in df_estoque.index:

        codigo = df_estoque['Item'][i]
        quantidade = df_estoque['Quantidade'][i]
        quantidade_nr = df_estoque['Qt não reservada'][i]

        flag = pd.isna(quantidade_nr)

        if flag != True:
            quantidade = quantidade_nr

        quantidade = quantidade.replace('.', '_')
        quantidade = quantidade.replace(',', '.')
        quantidade = quantidade.replace('_', '')

        quantidade = float(quantidade)

        codigos.append(codigo)
        quantidades.append(quantidade)

    for i in df_mangueiras.index:

        codigo = df_mangueiras['Código do item'][i]
        quantidade = str(df_mangueiras['Quantidade contada (metros)'][i])
        
        quantidade = quantidade.replace('.', ',')
        quantidade = quantidade.replace(',', '.')

        quantidade = float(quantidade)

        codigos.append(codigo)
        quantidades.append(quantidade)

    df_estoque = pd.DataFrame({'CODIGOS': codigos, 'QUANTIDADES': quantidades})
    #print(df_estoque)
    df_estoque_agrupado = df_estoque.groupby('CODIGOS', as_index=False)['QUANTIDADES'].sum()
    #print(df_estoque_agrupado)

    itens = []
    for i in df_estoque_agrupado.index:

        item = []
        codigo = df_estoque_agrupado['CODIGOS'][i]
        quantidade = df_estoque_agrupado['QUANTIDADES'][i]
        quantidade = float(quantidade)

        #if codigo == '10643-24-24':
            #print(int(quantidade), i)
        
        item=['flag',codigo,int(quantidade)]
        itens.append(item)

    return itens

def generate_document(itens, csv_name):

    print('Gerando documento...')

    with open(csv_name, 'w', newline='') as datas:
        writer_object = writer(datas)
        writer_object.writerow(["PARTNUMBER;QUANTIDADE;VALOR"])

        for item in itens:

            new_item = item[1].replace("_"," ")
            writer_object = writer(datas)
            writer_object.writerow([f'{new_item};{item[2]};*Sob Consulta'])

    datas.close()
    return