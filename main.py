import pandas as pd
import utils

from datetime import datetime
from weather import buscar_clima



def main():
    avistamentos_jacutinga = utils.read_csv("data/exemplo.csv")
  

    # Configurações
    API_KEY = "5e164d17260da778da3bcb39b35aea95"
    
    #Lista vazia para armazenar os dados
    dados = []
   
    # Buscando dados para uma data
    
    for avistamento in avistamentos_jacutinga:
        latitude = avistamento["latitude"]
        longitude = avistamento["longitude"]
        data_str = avistamento["data_hora"]
    
       # Converter a string de data para um objeto datetime
        data_hora = datetime.strptime(data_str, "%Y-%m-%d %H:%M:%S")
    
        # Buscar os dados climáticos
       
        avistamento_clima = buscar_clima(latitude, longitude, data_hora, API_KEY) 
        #juntar avistamento com busca clima
        registro_completo = {**avistamento, **avistamento_clima}
        
        #juntar avistamento com avistamento_clima antes de fazer o append
        #abrir um pull request e marcar felipe como revisor
        #dados.append(x)
        dados.append(registro_completo)
    df = pd.DataFrame(dados)  

    print(df.groupby("nome_ave").agg({"temperatura": ["mean", "min", "max"]}))     


if __name__ == "__main__":
    main()
