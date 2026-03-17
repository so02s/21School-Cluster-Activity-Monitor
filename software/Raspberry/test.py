import requests
from requests.structures import CaseInsensitiveDict

url = "https://auth.21-school.ru/auth/realms/EduPowerKeycloak/protocol/openid-connect/token"

headers = CaseInsensitiveDict()
headers["Content-Type"] = "application/x-www-form-urlencoded"

data = {
    "client_id": "s21-open-api",
    "username": "",
    "password": "",
    "grant_type": "password"
}

response = requests.post(url, headers=headers, data=data)

if response.status_code == 200:
    print("Токен получен успешно!")
    print(response.json())
else:
    print(f"Ошибка {response.status_code}: {response.text}")