from json import dumps
import requests
import os
import time

"""f1 = F1(secure=True)
pilotos = f1.all_drivers().json
with open('pilotos/pilotos.json', 'w') as f:
    f.write(dumps(pilotos))
"""


class Response:

    def __init__(self, formato: str = 'json'):
        self.formato = formato
        self.url = 'https://ergast.com/api/f1/'

    def request(self, qual_info: str, limit: int = None, offset: int = None):

        if limit != None:
            parametros = {'limit': limit, 'offset': offset}
        else:
            parametros = None
        return requests.get(self.url+qual_info+'.'+self.formato, params=parametros)


class Formula1:

    def __init__(self):
        self.conexao = Response()

    def todos_pilotos(self, limite: int = 853, offset: int = 0):
        try:
            os.mkdir('pilotos')
        except FileExistsError:
            print("O diretório já existe")
        time.sleep(2)

        pilotos = self.conexao.request(
            'drivers', limit=limite, offset=offset).json()
        try:
            with open('pilotos/todos_pilotos.json', 'w') as f:
                f.write(dumps(pilotos))
        except FileNotFoundError:
            print("Não foi possível criar o arquivo")