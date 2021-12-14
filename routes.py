from app import app
from marcas import funcoes_gaudi, funcoes_elizabeth, funcoes_level, funcoes_porto_ferreira, funcoes_lexxa,funcoes_sense,funcoes_belgotex
from funcoes_aplicacao import verifica_arquivo_pdf



@app.route('/api/v1/atualizacaoestoque/<string:marcas>', methods=["GET","POST"])
def get_marcas(marcas):
    valuemarcas = str(marcas).lower().strip()
    verifica_arquivo_pdf(valuemarcas)
    print(verifica_arquivo_pdf(valuemarcas))

    if 'gaudi' in valuemarcas:
        print(valuemarcas)
        jsons = funcoes_gaudi(valuemarcas)
        return jsons

    elif 'elizabeth' in valuemarcas:
        jsons = funcoes_elizabeth(valuemarcas)
        print(valuemarcas)
        return jsons

    elif 'level' in valuemarcas:
        jsons = funcoes_level(valuemarcas)
        print(valuemarcas)
        return jsons

    elif 'portoferreira' in valuemarcas:
        try:
            marcapf = valuemarcas.replace(" ","")
            jsons = funcoes_porto_ferreira(marcapf)
            print(marcapf)
            return jsons
        except:
            print("nao tem")

    elif 'lexxa' in valuemarcas:
        jsons = funcoes_lexxa(valuemarcas)
        print(valuemarcas)
        return jsons

    elif 'sense' in valuemarcas:
        jsons = funcoes_sense(valuemarcas)
        print(valuemarcas)
        return jsons

    elif 'belgotex' in valuemarcas:
        jsons = funcoes_belgotex(valuemarcas)
        print(valuemarcas)
        return jsons






