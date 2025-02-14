import requests


def push_maxi(token, pagina, url):

    parametros = {
        'token': token,
        'PaginaAtual': pagina,
        'TamanhoDePagina': '5000'
    }
    response = requests.get(url, params=parametros)
    data = response.json() 
    return data