from pdf2image import convert_from_path, convert_from_bytes
import tempfile
import cv2
import pytesseract
import re
import pandas as pd
from itertools import zip_longest
from os import listdir, path, makedirs
from os.path import isfile, join
import time
# path Pytesseract
import os
import sys
import glob
import pyodbc
import numpy as np
from datetime import date

elizabeth = 'elizabeth'

filename = elizabeth + " - " + \
           time.strftime("%d-%b").replace(":", ".") + ".csv"

path = 'D:\\planilhasestoquesatualizacaodiaria\\Planilhas criadas\\'
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
          WHERE PM.Marca = 'Elizabeth'

    """

df = pd.read_sql_query(select_bd, conn)

elizabeth = 'elizabeth'
filename = elizabeth + " - " + \
           time.strftime("%d-%b").replace(":", ".") + ".csv"

pytesseract.pytesseract.tesseract_cmd = 'C:\\Users\\Crawler\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe'

data_atual = str(date.today())


imagens_files = 'D:\\Trabalhos Python\\converter_pdffiles\\imagemelizabeth\\'

# converter pdf em jpg


items = []
lista_referencias = []
lista_saldos = []
lista_prazos = []

refs = []
saldo = []


def ajuste_numeros(ref, num):
    cont = len(ref)
    if cont == 13 and "," in num:
        valor = ref.strip()
        refs.append(valor)
        saldo.append(num)

files = []
try:
    arquivos = os.listdir('D:\\Trabalhos Python\\converter_pdffiles\\')
    for arquivo in arquivos:
        if "elizabeth" and ".pdf" in arquivo:
            if data_atual in arquivo:
                files.append(arquivo)

    pdf_elizabeth = files[0]

    file_pdf = f'D:\\Trabalhos Python\\converter_pdffiles\\elizabeth\\{pdf_elizabeth}'

    # converte pdf em imagem
    images = convert_from_path(file_pdf, 200, poppler_path='D:\\Trabalhos Python\\converter_pdffiles\\poppler-21.10.0\\Library\\bin')
    for i in range(len(images)):
        images[i].save(imagens_files + 'elizabeth' + str(i) + '.jpg', 'JPEG')
except:
    pass


# ajuste texto
def ajuste_strings(elementos):
    referencia = []
    saldo = []

    valor = elementos.replace("[", "").replace("_|",
                                               "").replace("|", "").replace("[|", "").replace("[",
                                                                                              "").replace("_",
                                                                                                          "").replace(
        "]", "").strip()
    ajuste = valor.split(" ")

    try:
        referencias = ajuste[1]
        referencia.append(referencias)
    except:
        referencia.append("Não encontrado")

    try:
        saldos = ajuste[-1]
        saldo.append(saldos)
    except:
        saldo.append("Não encontrado")

    return referencia, saldo


# faz a busca das imagens na pasta e realiza a leitura e aplica filtro e posterior converção para string
imagens_convert = [f for f in listdir(imagens_files) if isfile(join(imagens_files, f))]
for imag in imagens_convert:
    imagem = cv2.imread(f'D:\\Trabalhos Python\\testes_aplicacao\\imagemelizabeth\\{imag}')
    imagem_gray = cv2.cvtColor(imagem, cv2.COLOR_RGB2GRAY)
    texto = pytesseract.image_to_string(imagem_gray)
    convert = texto.split("\n")
    remov_esp = [x.strip() for x in convert if x != ' ' if x != '']
    for remov in remov_esp:
        ref, sd = ajuste = ajuste_strings(remov)
        for x, y in zip_longest(ref, sd):
            lista_referencias.append(x)
            lista_saldos.append(y)
            lista_prazos.append(np.nan)


def converte_infos():
    try:
        df_elizabeth = pd.DataFrame({"Referencias": lista_referencias, "Saldos": lista_saldos})
    except Exception as e:
        print(e)
        print("Erro Dataframe")

    try:
        df_elizabeth[["Referencias", "Saldos"]].apply(lambda x: ajuste_numeros(x["Referencias"], x["Saldos"]), axis=1)
    except Exception as e:
        print(e)
        print("Erro função")

    try:
        df_ajuste = pd.DataFrame({"CodigoProduto": refs, "Saldo": saldo})
        df_ajuste["CodigoProduto"] = df_ajuste["CodigoProduto"].astype(str)
    except Exception as e:
        print(e)
        print("Erro Dataframe Ajuste")

    try:
        final_df = pd.merge(df, df_ajuste, left_on='SKU', right_on='CodigoProduto', how='left')
        final_df = final_df[["IdMarca", "SKU", "NomeProduto", "Marca", "Saldo"]]
        final_df["Saldo"].fillna(0, inplace=True)
        final_df["Prazo"] = np.nan
        final_df = final_df[["IdMarca", "SKU", "Saldo", "Prazo"]]
    except Exception as e:
        print(e)
        print("Erro dataframe merge")
    try:
        final_df = final_df.drop_duplicates()
        elizabeth = final_df.to_json(orient='records')
        return elizabeth
    except Exception as e:
        return {"Valor":"Não encontrado"}






