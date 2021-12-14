import numpy as np
from pdf2image import convert_from_path, convert_from_bytes
import tempfile
import cv2
import pytesseract
import re
import pandas as pd
from itertools import zip_longest
from os import listdir, path, makedirs
from os.path import isfile, join
import shutil
import pyodbc
import time
from itertools import zip_longest
from datetime import date
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
          WHERE PM.Marca = 'Gaudi'

    """

gaudi = 'gaudi_layou3'
filename = gaudi + " - " + \
           time.strftime("%d-%b").replace(":", ".") + ".csv"
df_bdhausz = pd.read_sql_query(select_bd, conn)

data_atual = str(date.today())

files = []

arquivos = os.listdir('D:\\Trabalhos Python\\converter_pdffiles\\gaudi\\')

for arquivo in arquivos:
    if "gaudi" and ".pdf" in arquivo:
        if data_atual in arquivo:
            files.append(arquivo)
try:
    pdf_gaudi = files[0]

    path = f'D:\\Trabalhos Python\\converter_pdffiles\\gaudi\\{pdf_gaudi}'
except:
    pass

pytesseract.pytesseract.tesseract_cmd = 'C:\\Users\\Crawler\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe'
    #pdf_file = f'D:\\Trabalhos Python\\converter_pdffiles\\{path}'
imagens_files = 'D:\\Trabalhos Python\\converter_pdffiles\\imagemgaudi\\'
imagens_gaudi = 'D:\\Trabalhos Python\\converter_pdffiles\\imagemgaudi\\'


def converte_pdf_imagem():
    try:
        # converte pdf em imagem
        images = convert_from_path(path, 200,
                                   poppler_path='D:\\Trabalhos Python\\converter_pdffiles\\poppler-21.10.0\\Library\\bin')
        for i in range(len(images)):
            images[i].save(imagens_gaudi + 'gaudi' + str(i) + '.jpg', 'JPEG')

    except:
        pass


def ajuste_referencias(elementos):
    ajustados = []
    for elemento in elementos:
        valor = elemento.replace(".", "").strip()
        ajustados.append(valor)

    return ajustados


def referencia_gaudi(elementos):
    try:
        valor = elementos[:4]
        return valor
    except Exception as e:
        print(e)
        return elementos


lista_referencia = []
lista__saldos = []
lista_prazos = []


# Separa referencias e saldos Gaudi
def separa_infos(elementos):
    referencias = []
    saldos = []
    for elemento in elementos:
        valor = elemento.split(" ")
        try:
            ref = valor[0]
            referencias.append(ref)
        except Exception as e:
            print(e)
            referencias.append("Valor não encontrado")
        try:
            saldo = valor[-3:]
            sd = saldo[0]
            saldos.append(sd)
        except Exception as e:
            print(e)
            saldos.append(0)

    return referencias, saldos


# trata quebra de linhas e remove valores desnecessários que podem atrapalhar no funcionamento da "separa_infos"
def ajuste_string(elementos):
    ajustados = []
    lista = []

    valor = elementos.split("\n")
    for val in valor:
        ajust = val.replace("Data:", "").replace("Pagina", "").replace("ESTOQUE",
                                                                       "").replace("ATUAL", "").replace("Produto",
                                                                                                        "").replace(
            "60X60", "").replace("61X61",
                                 "").replace("80X80", "").replace("81X81",
                                                                  "").replace("ESTOQUE", "").replace("ATUAL",
                                                                                                     "").strip()
        lista.append(ajust)

    ajuste = [x for x in lista if x != '' if x != ' ']
    for aj in ajuste:
        ajustados.append(aj)
    return ajustados


def leitura_imagem():
    lista_imagens_all = [f for f in listdir(imagens_files) if isfile(join(imagens_files, f))]
    for imag in lista_imagens_all:
        try:
            imagem = cv2.imread(f'D:\\Trabalhos Python\\converter_pdffiles\\imagemgaudi\\{imag}')
            imagem_gray = cv2.cvtColor(imagem, cv2.COLOR_RGB2GRAY)
            texto = pytesseract.image_to_string(imagem_gray)

        except Exception as e:

            print(e)
            print("Erro não conversão")

        strings = ajuste_string(texto)
        refs, sald = separa_infos(strings)
        for x, y in zip_longest(refs, sald):
            lista_referencia.append(x)
            lista__saldos.append(y)
            lista_prazos.append(np.nan)


def converte_infos():
    converte_pdf_imagem()
    leitura_imagem()

    try:
        df_gaudi = pd.DataFrame({"Referencias": lista_referencia, "Saldos": lista__saldos, "Prazo": lista_prazos})
        df_gaudi["Referencias"] = ajuste_referencias(df_gaudi["Referencias"])
    except Exception as e:
        print(e)
        print("Erro criação Dataframe Gaudi")
    caminho = 'D:\\Trabalhos Python\\'
    try:
        df_bdhausz["referencia_gaudi"] = df_bdhausz["SKU"].apply(lambda x: referencia_gaudi(x))
        final_df = pd.merge(df_bdhausz, df_gaudi, left_on='referencia_gaudi', right_on='Referencias', how='left')
        final_df = final_df[["IdMarca", "SKU", "Saldos", "Prazo"]]
        final_df["Saldos"].fillna(0, inplace=True)
        final_df["Prazo"] = final_df["Prazo"].astype(float)
        final_df = final_df.drop_duplicates()
        final_df.to_excel(caminho + "teste_leituragaudi.xlsx")

        jsons = final_df.to_json(orient='records')
        print(jsons)
        return jsons
    except Exception as e:
        print(e)
        return {"Valor":"Não encontrado"}









