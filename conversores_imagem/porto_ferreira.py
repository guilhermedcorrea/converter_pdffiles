import pandas as pd
import pyodbc
import os
import numpy as np
from datetime import date

conn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                      "Server=w2019.hausz.com.br;"
                      "Database=HauszMapa;"
                      "UID=Aplicacao;"
                      "PWD=S3nh4Apl!caca0")

select_bd = """
        SELECT 
        PZ.[SKU]
          ,P_B.IdMarca
          ,P_B.NomeProduto
          ,P_B.IdProduto
          ,PM.Marca
          ,P_B.EAN
          FROM [HauszMapa].[Produtos].[ProdutoPrazoProducFornec] AS PZ
          JOIN Produtos.ProdutoBasico as P_B
          ON P_B.SKU = PZ.SKU
          JOIN Produtos.Marca AS PM
          ON PM.IdMarca = P_B.IdMarca
          JOIN V_ConsultaSaldo AS V_C
          ON V_C.IdProduto = P_B.IdProduto
          WHERE PM.Marca = 'Porto Ferreira'

    """


def ajuste_referencia_sku(elementos):
    try:
        ajustados = []
        for elemento in elementos:
            valor = str(elemento)
            sku = valor[:-1]+'PF'
            ajustados.append(sku)
        return ajustados
    except:
        pass

def converte_infos():
    lista_file = []
    data = str(date.today())
    try:
        arquivos = os.listdir('D:\\Trabalhos Python\\converter_pdffiles\\')
        for arquivo in arquivos:
            if 'portoferreira' and '.xls' and data in arquivo:
                lista_file.append(arquivo)
    except Exception as e:
        print(e)

    try:
        files = lista_file[0]
        path = f'D:\\Trabalhos Python\\converter_pdffiles\\{files}'
        df_porto = pd.read_excel(path)

        df_porto = df_porto[["Produto","Disponível"]]
        df_porto['Produto'] = df_porto['Produto'].fillna(method='pad')
        df_porto["Disponível"].fillna(0,inplace=True)
        df_porto["Disponível"] = df_porto["Disponível"].astype(float)
        df_porto["Produto"] = df_porto["Produto"].astype(str)
        df_porto = df_porto.sort_values('Disponível', ascending=False).drop_duplicates('Produto').sort_index()
        df_porto["Prazo"] = np.nan
        df_porto["Produto"] = ajuste_referencia_sku(df_porto["Produto"])


        df_bdhausz = pd.read_sql_query(select_bd, conn)
        final_df = pd.merge(df_bdhausz, df_porto, left_on='SKU', right_on='Produto', how='left')
        final_df["Disponível"].fillna(0,inplace=True)
        final_df = final_df.rename(columns={"Disponível":"Saldo"})
        final_df = final_df[["IdMarca", "SKU", "Saldo", "Prazo"]]
        final_df = final_df.drop_duplicates()
        json_porto = final_df.to_json(orient='records')

        print(json_porto)

        return json_porto
    except:
        return {"Valor":"Não encontrado"}


