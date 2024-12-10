import requests

from datetime import datetime







# acessando a API usando python
# https://api.openweathermap.org/data/3.0/onecall/timemachine?lat=-22.9108074&lon=-45.9573599&dt=2024-10-01&appid=5e164d17260da778da3bcb39b35aea95 

endpoint = "https://api.openweathermap.org/data/3.0/onecall/timemachine"

latitude = -22.9108074

longitude = -45.9573599

data_str = "2024/10/01"
 #https://openweathermap.org/api/one-call-3

data = datetime.strptime(data_str, '%Y/%m/%d')

TOKEN = "5e164d17260da778da3bcb39b35aea95"
# lat=-22.9108074&lon=-45.9573599&dt=2024-10-01&appid=5e164d17260da778da3bcb39b35aea95 
latitude = -22.9108074
url = f"{endpoint}?lat={latitude}&lon={longitude}&dt={int(data.timestamp())}&appid={TOKEN}"

print(url)
response = requests.get(url)
print(response.text)