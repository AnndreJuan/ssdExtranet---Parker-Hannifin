from ..connection_erp.use_case import push_maxi
from csv import writer
import pandas as pd
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
__TOKEN = os.getenv("TOKEN")

def update_data_companies(url, csv_name):
    # Updates the companies dataframe

    print('Generating Companies File...')

    data = push_maxi(__TOKEN, 1, url)
    total_pages = data['QuantidadeDePaginas']
    
    with open(csv_name, 'w', newline='') as file:
        writer_object = writer(file)
        writer_object.writerow(["COMPANY_ID;COMPANY_NAME;TAX_ID;EMAIL;NICKNAME"])
        for page in range(1, total_pages + 1):
            data = push_maxi(__TOKEN, page, url)
            for item in data['Registros']:
                writer_object = writer(file)
                company_name = str(item["Razao_social"])

                company_name = company_name.replace(',', '')
                company_name = company_name.replace(';', '')
                company_name = company_name.replace('\n', '')
                
                writer_object.writerow([
                    f'{item["Empresa_Id"]};{company_name};{str(item["CNPJ_CPF"])};{str(item["Email"])};{item["Apelido"]}'
                ])

def update_data_items(url, csv_name):
    # Updates the items dataframe

    print('Generating Items File...')
    data = push_maxi(__TOKEN, 1, url)
    total_pages = data['QuantidadeDePaginas']
    
    with open(csv_name, 'w', newline='') as file:
        writer_object = writer(file)
        writer_object.writerow(["ITEM_ID;CODE;COMPANY;GROUP_ID;UNIT_OF_MEASURE"])
        for page in range(1, total_pages + 1):
            data = push_maxi(__TOKEN, page, url)
            for item in data['Registros']:  
                writer_object = writer(file)
                writer_object.writerow([
                    f'{item["Item_Id"]};{item["Codigo"]};HPC;{item["Grupo_Id"]};{item["Unidade_principal"]}'
                ])

def update_data_stock(url, csv_name):
    # Updates the stock data

    print('Generating Stock File...')
    df_companies = pd.read_csv('./files/Companies_Maxi.csv', encoding='latin-1', sep=';', on_bad_lines='skip')
    data = push_maxi(__TOKEN, 1, url)
    total_pages = data['QuantidadeDePaginas']
    
    with open(csv_name, 'w', newline='') as file:
        writer_object = writer(file)
        writer_object.writerow(["ITEM_ID;PRODUCT_TYPE;COMPANY;STOCK;STOCK_LOCATION"])

        for page in range(1, total_pages + 1):
            data = push_maxi(__TOKEN, page, url)
            for item in data['Registros']:
                if (item["Estoque"] == "Matéria-prima" and 
                    item["EnderecoEstoque_codigo"] is not None and 
                    item["EnderecoEstoque_descricao"] != "SIMILAR"): 
                    
                    writer_object = writer(file)
                    
                    # Get the company nickname from the companies dataframe
                    company_stock = df_companies.loc[
                        df_companies['EMPRESA_ID'] == str(item["Propria_empresa_Id"]), 'APELIDO'
                    ]
                    company_stock = company_stock.tolist()
                    company_stock = company_stock[0] if company_stock else ''

                    # Translate product type if needed
                    product_type = "Raw Material" if item["Estoque"] == "Matéria-prima" else item["Estoque"]

                    writer_object.writerow([
                        f'{item["Item_Id"]};{product_type};{company_stock};{item["Quantidade"]};{item["EnderecoEstoque_codigo"]}'
                    ])

def analyze_data():
    # Analyzes the stock and items data

    print('Analyzing Data...')
    items_list = []

    df_stock = pd.read_csv('./files/Items_Stock.csv', encoding='latin-1', sep=';')
    df_items = pd.read_csv('./files/Items_Maxi.csv', encoding='latin-1', sep=';')

    df_stock_grouped = df_stock.groupby('ITEM_ID')['STOCK'].sum().reset_index()
    print(df_stock_grouped.head())

    for i in df_stock_grouped.index:
        item_id = df_stock_grouped['ITEM_ID'][i]
        stock_quantity = df_stock_grouped['STOCK'][i]
        stock_quantity = int(round(stock_quantity, 2))

        # Look for the corresponding code
        code_series = df_items.loc[df_items['ITEM_ID'] == item_id, 'CODE']
        code_list = code_series.to_list()

        if not code_list:
            # If no code is found, display a message and skip to the next item.
            print(f"ITEM_ID {item_id} not found in df_items.")
            continue

        code = code_list[0]
        
        item_add = [item_id, code, stock_quantity]
        items_list.append(item_add)

    return items_list

def generate_document(items, csv_name):
    # Generates the final document

    print('Generating Document...')

    with open(csv_name, 'w', newline='') as file:
        writer_object = writer(file)
        writer_object.writerow(["PARTNUMBER;QUANTITY;PRICE"])

        for item in items:
            partnumber = item[1].replace("_", " ")
            writer_object = writer(file)
            writer_object.writerow([f'{partnumber};{item[2]};*Price on Request'])
    file.close()
