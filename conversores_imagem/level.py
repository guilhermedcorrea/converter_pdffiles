from typing import final
import pandas as pd
import pyodbc
import time
from datetime import date
from datetime import datetime
import numpy as np
import os

path = 'D:\\planilhasestoquesatualizacaodiaria\\Planilhas criadas\\'
level = 'level'
filename = level + " - " + \
           time.strftime("%d-%b").replace(":", ".") + ".csv"

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
          WHERE PM.Marca = 'Level'

    """


def ajuste_saldo(elementos):
    digitos = []
    for elemento in elementos:
        valor = round(elemento, 2)
        digitos.append(valor)

    return digitos


def ajuste_data(elementos):
    datas = []
    for elemento in elementos:
        valor = elemento.split("-")
        ano = str(valor[0])
        mes = str(valor[1:2])
        dia = str(valor[2:3])

        data = dia + "/" + mes + "/" + ano
        datas.append(data)
    return datas


def ajuste_previsão(elementos):
    alterados = []
    for elemento in elementos:
        valor = elemento.replace("['", "").replace("']", "").replace("[]/[]/NaT", "0")
        alterados.append(valor)

    return alterados


def ajusta_codigo(elementos):
    codigos = []
    for elemento in elementos:
        valor = str(elemento) + 'L'
        codigos.append(valor)

    return codigos


def ajuste_datas(elementos):
    lista_ajustado = []
    for elemento in elementos:
        valor = str(elemento)
        if "/" in valor:
            lista_ajustado.append(valor)

        else:
            lista_ajustado.append(np.nan)

    return lista_ajustado


def datas(elementos):
    data_atual = date.today()
    datas_ajustadas = []
    ajustados = []
    for elemento in elementos:
        valor = str(elemento).split(" ")
        ajustados.append(valor[0])

    dates = str(data_atual)
    datas_replace = [x.replace("NaT", dates) for x in ajustados]
    for data in datas_replace:
        datas_ajustadas.append(data)
    return datas_ajustadas


def remove_zeros_negativos(elementos):
    ajustados = []
    for elemento in elementos:
        valor = str(elemento).split(" ")
        dias = valor[0]
        if "-" in dias:
            ajustados.append(np.nan)
        elif "0" in dias:
            ajustados.append(np.nan)
        else:
            ajustados.append(dias)

    return ajustados


def ajuste_referencias(elementos):
    ajustados = []
    for elemento in elementos:
        valor = str(elemento).replace(".0", "")
        ajustados.append(valor)
    return ajustados


def converte_infos():
    arquivo = os.listdir('D:\\Trabalhos Python\\converter_pdffiles\\level\\')
    files = arquivo[0]

    path = f'D:\\Trabalhos Python\\converter_pdffiles\\level\\'
    try:
        level_df = pd.ExcelFile(path + files)
        level_df.sheet_names

    except Exception as e:
        print(e)
        print("Planilha nao encontrada")

    sheet_to_df_map = []
    for sheet_name in level_df.sheet_names:
        sheet_to_df_map.append(level_df.parse(sheet_name))

    unificar = pd.concat(sheet_to_df_map)

    unificar = unificar[["Código", "Estoque", "Previsão*"]]
    unificar["Código"] = ajuste_referencias(unificar["Código"])
    unificar["Código"] = ajusta_codigo(unificar["Código"])
    unificar["Estoque"] = ajuste_saldo(unificar["Estoque"])
    unificar["Estoque"] = unificar["Estoque"].astype(float)
    unificar["Previsão*"] = unificar["Previsão*"].astype(str)
    unificar["Previsão*"] = ajuste_data(unificar["Previsão*"])
    unificar["Previsão*"] = ajuste_previsão(unificar["Previsão*"])
    unificar["Previsão*"] = unificar["Previsão*"].astype(str)
    unificar["Estoque"].fillna(0, inplace=True)
    unificar = unificar.sort_values('Estoque', ascending=False).drop_duplicates('Código').sort_index()
    df_bdhausz = pd.read_sql_query(select_bd, conn)
    finall_df = pd.merge(df_bdhausz, unificar, left_on='SKU', right_on='Código', how='left')
    finall_df["Previsão*"] = ajuste_datas(finall_df["Previsão*"])
    finall_df["Previsão*"] = finall_df["Previsão*"].astype('datetime64[ns]')
    finall_df["Previsão*"] = datas(finall_df["Previsão*"])
    data_atual = date.today()
    finall_df["DataAtual"] = data_atual
    finall_df["Previsão*"] = finall_df["Previsão*"].astype('datetime64[ns]')
    finall_df["DataAtual"] = finall_df["DataAtual"].astype('datetime64[ns]')
    finall_df["Prazo"] = finall_df["Previsão*"] - finall_df["DataAtual"]
    finall_df["Prazo"] = remove_zeros_negativos(finall_df["Prazo"])
    finall_df["Estoque"] = finall_df["Estoque"].astype(float)
    finall_df["Prazo"] = finall_df["Prazo"].astype(float)
    finall_df = finall_df.drop_duplicates()
    finall_df = finall_df[["IdMarca", "SKU", "Estoque", "Prazo"]]
    finall_df["Estoque"].fillna(0, inplace=True)
    jsons = finall_df.to_json(orient='records')
    return jsons
    print(jsons)


