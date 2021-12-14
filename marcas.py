
from controllers import *
from funcoes_aplicacao import verifica_arquivo_pdf
from converter_pdffiles.conversores_imagem import gaudi,elizabeth, level, porto_ferreira, lexxa, sense, belgotex


def funcoes_gaudi(elementos):

    consulta_ftp(elementos)
    verifica_arquivo_pdf(elementos)
    jsons = gaudi.converte_infos()
    print(jsons)
    return jsons

def funcoes_elizabeth(elementos):

    consulta_ftp(elementos)
    verifica_arquivo_pdf(elementos)
    jsons = elizabeth.converte_infos()
    print(jsons)
    return jsons

def funcoes_level(elementos):
    consulta_ftp(elementos)
    verifica_arquivo_pdf(elementos)
    jsons = level.converte_infos()
    print(jsons)
    return jsons

def funcoes_porto_ferreira(elementos):
    valuee = consulta_ftp(elementos)
    print(valuee)
    try:
        verifica_arquivo_pdf(elementos)
        jsons = porto_ferreira.converte_infos()
        print(jsons)
        return jsons
    except:
        print("Nao tem")


def funcoes_lexxa(elementos):
    consulta_ftp(elementos)
    verifica_arquivo_pdf(elementos)
    jsons = lexxa.converte_infos()
    print(jsons)
    return jsons

def funcoes_sense(elementos):
    consulta_ftp(elementos)
    verifica_arquivo_pdf(elementos)
    jsons = sense.converte_infos()
    print(jsons)
    return jsons


def funcoes_belgotex(elementos):
    consulta_ftp(elementos)
    verifica_arquivo_pdf(elementos)
    jsons = belgotex.converte_infos()
    print(jsons)
    return jsons
