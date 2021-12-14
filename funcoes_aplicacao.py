import ftplib
import re
from os import listdir, path, makedirs
from os.path import isfile, join
import shutil
import os
from datetime import date



data_atual = date.today()


def consulta_ftp():
    HOSTNAME = "w2019.hausz.com.br"
    USERNAME = "Aplicacao"
    PASSWORD = "S3nh4Aplic4cao!"
    dirname = 'atualizacaoMarcaPDF'
    filename = 'Gaudi-2021-12-02-gaudi.pdf'
    savedir = 'D:\\Trabalhos Python\\testes_aplicacao\\'
    ftp = ftplib.FTP(HOSTNAME, USERNAME, PASSWORD)
    ftp.cwd('atualizacaoMarcaPDF')  # seta diretorio
    ftp.dir()  # exibe diretorios
    with open(filename, "wb") as file:
        ftp.retrbinary(f"RETR {filename}", file.write)



def verifica_arquivo_pdf(elementos):
    data = str(data_atual)
    pasta_atual = 'D:\\Trabalhos Python\\converter_pdffiles\\'
    mover = f'D:\\Trabalhos Python\\converter_pdffiles\\{elementos}\\'
    files = os.listdir('D:\\Trabalhos Python\\converter_pdffiles\\')

    for file in files:
        if ".pdf" in file:
            if re.search(f'{elementos}', file):
                print(file)

                if data in file:
                    shutil.move(pasta_atual+f'{file}', mover+f'{file}')
                try:
                    arquivo = os.listdir(f'D:\\Trabalhos Python\\converter_pdffiles\\{elementos}\\')
                    return arquivo[0]
                except:
                    pass

        elif ".xlsx" in file:
            if re.search(f'{elementos}', file):

                print(file)
                if data in file:
                    shutil.move(pasta_atual + f'{file}', mover + f'{file}')
                try:
                    arquivo = os.listdir(f'D:\\Trabalhos Python\\converter_pdffiles\\{elementos}\\')
                    return arquivo[0]
                except:
                    pass

        elif ".csv" in file:
            if re.search(f'{elementos}', file):
                print(file)
                if data in file:
                    shutil.move(pasta_atual + f'{file}', mover + f'{file}')
                try:
                    arquivo = os.listdir(f'D:\\Trabalhos Python\\converter_pdffiles\\{elementos}\\')
                    return arquivo[0]
                except:
                    pass















