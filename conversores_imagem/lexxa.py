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
import os
import numpy as np
import sys
import shutil



lista_referencias = []
lista_saldos = []
lista_prazos = []

lexxa = 'lexxa'
filename = lexxa + " - " + \
           time.strftime("%d-%b").replace(":", ".") + ".csv"
try:
    path = 'D:\\Trabalhos Python\\converter_pdffiles\\'
except:
    pass
pytesseract.pytesseract.tesseract_cmd = 'C:\\Users\\Crawler\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe'


imagens_files = 'D:\\Trabalhos Python\\converter_pdffiles\\imagemlexxa\\'
imagens_lexxa = 'D:\\Trabalhos Python\\converter_pdffiles\\imagemlexxa\\'


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
          WHERE PM.Marca = 'Lexxa'

    """


def testeteste(elementos):
    referencia = []
    saldo = []

    for elemento in elementos:
        valor = elemento.split(" ")
        try:
            referencia.append(valor[0].strip())
        except Exception as e:
            print(e)
            referencia.append("Não encontrado")

        try:
            saldo.append(valor[-1].replace(".","").replace("PC",""))
        except Exception as e:
            print(e)
            saldo.append("Não encontrado")

    return referencia, saldo
try:
    arquivo = os.listdir('D:\\Trabalhos Python\\converter_pdffiles\\lexxa\\')
    files = arquivo[0]

    pdf_file = f'D:\\Trabalhos Python\\converter_pdffiles\\lexxa\\{files}'

    images = convert_from_path(pdf_file, 200, poppler_path='D:\\Trabalhos Python\\converter_pdffiles\\poppler-21.10.0\\Library\\bin')
    for i in range(len(images)):
        images[i].save(imagens_lexxa + 'lexxa' + str(i) + '.jpg', 'JPEG')
except Exception as e:
    print(e)
    print("Erro caminho pdf lexxa")

lista_imagens_all = [f for f in listdir(imagens_files) if isfile(join(imagens_files, f))]

imagens_convert = [f for f in listdir(imagens_lexxa) if isfile(join(imagens_lexxa, f))]
for imag in imagens_convert:
    try:
        imagem = cv2.imread(f'D:\\Trabalhos Python\\converter_pdffiles\\imagemlexxa\\{imag}')

        imagem_gray = cv2.cvtColor(imagem, cv2.COLOR_RGB2GRAY)

    except Exception as e:
        print(e)
        print("Erro leitura imagem lexxa")

    texto = pytesseract.image_to_string(imagem_gray)
    values = texto.split("\n")
    remov_esp = [x.strip() for x in values if x != '' if x != ' ' if x != '']
    ref, sd = testeteste(remov_esp)
    for x, y in zip_longest(ref, sd):
        lista_referencias.append(x)
        lista_saldos.append(y)
        lista_prazos.append(np.nan)



def converte_infos():
    try:
        df_lexxa = pd.DataFrame({"Referencia": lista_referencias, "Saldo": lista_saldos,"Prazo":lista_prazos})
        df_bdhausz = pd.read_sql_query(select_bd, conn)
        final_df = pd.merge(df_bdhausz, df_lexxa, left_on='SKU', right_on='Referencia', how='left')
        final_df = final_df[["IdMarca", "SKU","Saldo","Prazo"]]
        final_df["Saldo"].fillna(0, inplace=True)
        final_df = final_df.drop_duplicates()

        jsons = final_df.to_json(orient='records')
        return jsons

    except Exception as e:
        return {"Valor":"Não encontrado"}








