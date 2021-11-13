import json


def somente_pilotos() -> dict:
    """Drivers: [
        {'driverId': str,
        'url': str,
        givenName: str,
        'familyName': str,
        'dateOfBirth': str,
        nationality: str}
    ]
    """
    try:
        with open('pilotos/todos_pilotos.json', 'r') as f:
            texto = f.read()
            dados = json.loads(texto)
    except FileNotFoundError as err:
        print("Arquivo não encontrado", err)
    pilotos = dados
    return pilotos['MRData']['DriverTable']