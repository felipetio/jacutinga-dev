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