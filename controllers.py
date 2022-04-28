import ftplib
import re
from os import chdir, getcwd, listdir
from os.path import isfile
from datetime import date

data_atual = date.today()


def file_names(elemento):
    base_string = str(elemento)
    search_string = ':'
    arquivo = base_string.find(search_string)
    name = base_string[arquivo:].split(" ")
    name[1:]
    unifica = " ".join(name[1:])
    return unifica.strip()


data_atual = date.today()


def file_names(elementos):
    valor = str(elementos).split(":")[-1]
    names = str(valor).split(" ")[1:]
    unifica = " ".join(names)
    return unifica


def consulta_ftp(elementos):
    lista_files = []
    HOSTNAME = ""
    USERNAME = ""
    PASSWORD = ""
    dirname = 'atualizacaoMarcaPDF'
    # filename = 'Gaudi-2021-12-02-gaudi.pdf'
    savedir = 'D:\\Trabalhos Python\\testes_aplicacao\\'
    ftp = ftplib.FTP(HOSTNAME, USERNAME, PASSWORD)
    ftp.cwd('atualizacaoMarcaPDF')  # seta diretorio
    arquivos_ajustados = []
    listas = []
    ftp.dir(listas.append)
    value_names = elementos.lower().replace(" ", "")

    for lst in listas:
        print(lst)
        lista = lst.lower()
        names = file_names(lista)
        if value_names in names:
            atual = str(data_atual)
            if atual in names:
                arquivos_ajustados.append(names)

    filename = arquivos_ajustados[0]
    print(filename)

    with open(filename, "wb") as file:
        ftp.retrbinary(f"RETR {filename}", file.write)
























