import pandas as pd
import utils
import requests
from datetime import datetime
from typing import Dict, Any, List
from conversor import kelvin_para_celsius

# URL base da API
OPENWEATERMAP_URL = "https://api.openweathermap.org"
    
def buscar_clima(latitude: float, longitude: float, data: datetime, api_key: str) -> Dict[str, Any]:
    """
    Busca dados climáticos para uma localização e data específicas
    See more: https://openweathermap.org/api/one-call-3#history
    
    Args:
        latitude (float): Latitude do local
        longitude (float): Longitude do local
        data (datetime): Data para buscar os dados
        api_key (str): Chave da API OpenWeatherMap
    Returns:
        Dict com dados formatados para uso com pandas
    """
    # Parâmetros da requisição
    params = {
        "lat": latitude,
        "lon": longitude,
        "dt": int(data.timestamp()), # Convertendo para timestamp como a API espera
        "appid": api_key,
    }
    
    url = OPENWEATERMAP_URL + "/data/3.0/onecall/timemachine"
    
    try:
        # Fazendo a requisição
        resposta = requests.get(url, params=params)
        resposta.raise_for_status()
        dados = resposta.json()
        
        # Extraindo dados relevantes
        clima = dados["data"][0]
        tempo = clima["weather"][0]
        
        # Formatando para pandas
        response = {
            "data": datetime.fromtimestamp(clima["dt"]),
            "latitude": dados["lat"],
            "longitude": dados["lon"],
            "temperatura": kelvin_para_celsius(clima["temp"]),
            "sensacao_termica": kelvin_para_celsius(clima["feels_like"]),
            "pressao": clima["pressure"],
            "umidade": clima["humidity"],
            "nuvens": clima["clouds"],
            "vento_velocidade": clima["wind_speed"],
            "vento_direcao": clima["wind_deg"],
            "nascer_sol": datetime.fromtimestamp(clima["sunrise"]),
            "condicao_clima": tempo["main"],
            "descricao_clima": tempo["description"],
            "por_sol": datetime.fromtimestamp(clima["sunset"]),
        }
        print(response)
        return response
    except requests.exceptions.HTTPError as e:
        raise Exception(f"Erro na requisição: {str(e)}")
    except (KeyError, ValueError) as e:
        raise Exception(f"Erro ao processar dados: {str(e)}")


# Exemplo de uso
def carregar_dados(file_name = "data/exemplo.csv"): 

    avistamentos_jacutinga = utils.read_csv(file_name)
  

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

    return df    

 
if __name__ == "__main__":
    # Exemplo de uso
    df = carregar_dados()
    print(df.head()) 
