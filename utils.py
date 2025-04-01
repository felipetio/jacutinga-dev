import csv

def read_csv(file_path: str) -> list[dict]:
    """ Essa Função lê UM arquivo CSV e retorna uma lista de dicionários
    """
    with open(file_path, 'r') as file:
        reader = list(csv.DictReader(file))
        
    return reader

           


