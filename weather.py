import requests






# acessando a API usando python
# https://api.openweathermap.org/data/3.0/onecall/timemachine?lat=-22.9108074&lon=-45.9573599&dt=2024-10-01&appid=5e164d17260da778da3bcb39b35aea95 

endpoint = "https://api.openweathermap.org/data/3.0/onecall/timemachine"

latitude = -22.9108074

logitude = -45.9573599

data = "2024-10-01"



TOKEN = "5e164d17260da778da3bcb39b35aea95"

url = f"{endpoint}?appid={TOKEN}"


response = requests.get(url)
print(response.text)