import re
import pandas as pd
from itertools import zip_longest
from os import listdir, path, makedirs
from os.path import isfile, join
import shutil
import pyodbc
import time
from itertools import zip_longest
import os
import numpy as np

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
          ,PM.Marca
          ,P_B.EAN
          FROM [HauszMapa].[Produtos].[ProdutoPrazoProducFornec] AS PZ
          JOIN Produtos.ProdutoBasico as P_B
          ON P_B.SKU = PZ.SKU
          JOIN Produtos.Marca AS PM
          ON PM.IdMarca = P_B.IdMarca
          JOIN V_ConsultaSaldo AS V_C
          ON V_C.IdProduto = P_B.IdProduto
          WHERE PM.Marca = 'Belgotex'

    """

referencias = []
saldos = []


def ajustes(elementos):
    for elemento in elementos:
        valor = str(elemento)
        if "HERCULES" in valor:
            nome = valor.split(" ")
            nomes = nome[1] + nome[-1]
            referencias.append(nomes)

        elif "ROCKY" in valor:
            nome = valor.split(" ")
            nomes = nome[1] + nome[-1]
            referencias.append(nomes)

        elif "CASTILLA" in valor:
            nome = valor.split(" ")
            nomes = nome[1] + nome[-1]
            referencias.append(nomes)

        elif "STONE" in valor:
            nome = valor.split(" ")
            nomes = nome[1] + nome[-1]
            referencias.append(nomes)

        elif "XL PU" in valor:
            nome = valor.split("-")
            nomes = nome[0]
            referencias.append(nomes)

        elif "CLASSIC MYSTIQUE" in valor:
            nome = valor.replace("/", "")
            referencias.append(nome)

        elif "P.SAFE" in valor:
            nome = valor.replace("P.SAFE", "Polysafe")
            referencias.append(nome)

        elif "CITY" in valor:
            nome = valor.split(" ")
            nomes = nome[1] + nome[2] + nome[3]
            referencias.append(nome)

        elif "ASTRAL" in valor:
            nome = valor.split(" ")
            nomes = nome[1] + nome[2]
            referencias.append(nomes)

        elif "INTERLUDE" in valor:
            nome = valor.split(" ")
            nomes = nome[1] + nome[2]
            referencias.append(nomes.replace("M.B./", ""))

        elif "EFFECTO" in valor:
            nome = valor.split(" ")
            nomes = nome[0] + nome[1]
            referencias.append(nomes)

        elif "SHADOW" in valor:
            nome = valor.split(" ")
            nomes = nome[1] + nome[2]
            referencias.append(nomes)

        elif "CONNECT" in valor:
            nome = valor.split(" ")
            nomes = nome[1] + nome[2]
            referencias.append(nomes)

        elif "LINEA" in valor:
            nome = valor.split(" ")
            nomes = nome[1] + nome[2]
            referencias.append(nomes)

        elif "ENTRADA" in valor:
            nome = valor.split(" ")
            nomes = nome[1] + nome[2]
            referencias.append(nomes)

        elif "AGREGATTA" in valor:
            nome = valor.split(" ")
            nomes = nome[1] + nome[2]
            referencias.append(nomes)

        elif "FRAGMENT" in valor:
            nome = valor.split(" ")
            nomes = nome[1] + nome[2]
            referencias.append(nomes)

        elif "FRINGE" in valor:
            nome = valor.split(" ")
            nomes = nome[1] + nome[2]
            referencias.append(nomes)

        elif "SOLIDUS" in valor:
            nome = valor.split(" ")
            nomes = nome[1] + nome[2]
            referencias.append(nomes)

        elif " 3 TONOS" in valor:
            nome = valor
            referencias.append(nome)

        elif "LAYOUT" in valor:
            nome = valor.split(" ")
            nomes = nome[0] + nome[1]
            referencias.append(nomes)

        elif "FORGE" in valor:
            nome = valor.split(" ")
            nomes = nome[1] + nome[2]
            referencias.append(nomes)

        else:
            referencias.append(valor)


def ajuste_saldo(elementos):
    for elemento in elementos:
        valor = str(elemento)

        if "> 1000" in valor:
            saldos.append("1000")

        elif "> 500" in valor:
            saldos.append("500")

        elif ">1000" in valor:
            saldos.append("1000")

        else:
            saldos.append("200")


def ajuste_nomes(elementos):
    ajustados = []
    for elemento in elementos:
        valor = str(elemento).replace("/", "").replace(" - DTS6299-E3", "").replace(" - DTS6297-E3",
                                                                                    "").replace(" - DTS6298-E3",
                                                                                                "").replace("4290",
                                                                                                            "").replace(
            "4330", "").replace("4360",
                                "").replace("MB", "").replace("KW", "").replace("KBW", "").replace(" ", "").strip()

        ajustados.append(valor)

    return ajustados


def ajusta_nomes_hausz(elementos):
    ajustados = []
    for elemento in elementos:
        valor = elemento.replace("Belgotex - Piso Vinilico", "").replace("em Manta",
                                                                         "").replace("2000 ", "").replace(
            "Preço por M²", "").replace("Belgotex - Carpete  ",
                                        "").replace("Belgotex - Carpete em Placa ", "").replace("Carpete em Placa ",
                                                                                                "").replace(
            "Piso Vinilico ", "").replace("Belgotex", "").replace("121,92x17,78", "").replace("60x60",
                                                                                              "").replace("50x50",
                                                                                                          "").replace(
            "121,92x17,78", "").replace("920", "").replace("50x100", "").strip().replace(" ", "").upper()

        ajustados.append(valor)

    return ajustados


def converte_infos():
    try:
        arquivo = os.listdir('D:\\Trabalhos Python\\converter_pdffiles\\belgotex\\')
        files = arquivo[0]

        path = f'D:\\Trabalhos Python\\converter_pdffiles\\belgotex\\'
        belgotex = pd.ExcelFile(path + files)

        belgotex.sheet_names
        sheet_to_df_map = {}
        for sheet_name in belgotex.sheet_names:
            sheet_to_df_map[sheet_name] = belgotex.parse(sheet_name)

        belgotex_unificado = pd.concat(sheet_to_df_map)
        belgotex_unificado["Unnamed: 0"] = ajustes(belgotex_unificado["Unnamed: 0"])
        belgotex_unificado["ESTOQUE"] = ajuste_saldo(belgotex_unificado["ESTOQUE"])
        belgotex_unificado["CARPETES EM PLACAS"] = ajustes(belgotex_unificado["CARPETES EM PLACAS"])
        belgotex_unificado["Estoque m2"] = ajuste_saldo(belgotex_unificado["Estoque m2"])

        nome_produtos = ajuste_nomes(referencias)

        df_bdhausz = pd.read_sql_query(select_bd, conn)
        df_bdhausz = df_bdhausz[["SKU", "IdMarca", "NomeProduto"]]
        df_bdhausz["NomeProduto"] = ajusta_nomes_hausz(df_bdhausz["NomeProduto"])
        df_bdhausz["NomeProduto"] = df_bdhausz["NomeProduto"].astype(str)

        belgotex_infos = pd.DataFrame({"NomeProduto": nome_produtos, "SALDO": saldos})
        belgotex_infos["NomeProduto"] = belgotex_infos["NomeProduto"].astype(str)

        finall_df = pd.merge(df_bdhausz, belgotex_infos, left_on='NomeProduto', right_on='NomeProduto', how='left')
        finall_df["Prazo"] = np.nan
        finall_df["SALDO"].fillna(0, inplace=True)
        finall_df = finall_df.drop_duplicates()

        finall_df = finall_df.rename(columns={"SALDO": "Estoque"})
        finall_df = finall_df[["IdMarca", "SKU", "Estoque", "Prazo"]]
        jsons = finall_df.to_json(orient='records')
        print(jsons)
        return jsons
    except Exception as e:
        return {"Valor":"Não encontrado"}


