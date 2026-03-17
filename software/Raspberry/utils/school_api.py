import time
import requests

class SchoolClient:
    def __init__(self, username: str, password: str,
                 url: str = "https://platform.21-school.ru/services/21-school/api",
                 auth_url: str = "https://auth.21-school.ru/auth/realms/EduPowerKeycloak/protocol/openid-connect/token",
                 client_id: str = 's21-open-api') -> None:
        """
        Url and auth_url might be changed
        """
        self.username = username
        self.password = password

        self.url = url
        self.auth_url = auth_url
        self.client_id = client_id
    
        self.token = None
        self.refresh_token = None
        self.expires_in = None

        # TODO might be changed
        # need func for refresh cluster_id
        self.clust_keys = {"at": 37074, "il": 34718, "mi": 34719,"oa": 34720}

        self.session = requests.Session()
        a = requests.adapters.HTTPAdapter(max_retries=5)
        self.session.mount('https://', a)
        self.session.mount('http://', a)

        self.session.headers.update({
            "Content-Type": "application/x-www-form-urlencoded"
        })

        self.get_token()

    def get_token(self, refresh_token: str = None) -> None:
        """
        Получение токена (и обновление, если предоставлен refresh_token)
        """
        if refresh_token:
            auth_data = {
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
                "client_id": self.client_id
            }
        else:
            auth_data = {
                "grant_type": "password",
                "username": self.username,
                "password": self.password,
                "client_id": self.client_id
            }

        response = self.session.post(self.auth_url, data=auth_data)

        if response.status_code != 200:
            raise Exception(f"Failed to get token, {response.status_code}")
        
        token_data = response.json()
        self.token = token_data["access_token"]
        self.refresh_token = token_data["refresh_token"]
        self.expires_in = time.time() + token_data["expires_in"]

        self.session.headers.update({
            "Authorization": f"Bearer {self.token}"
        })

    def get(self, url, params=None) -> None:
        if self.is_token_expired():
            self.get_token(self.refresh_token)

        response = self.session.get(url, params=params)

        if response.status_code == 401:
            self.get_token(self.refresh_token)
            return self.get(url, params)
        elif response.status_code == 200:
            return response.json()
        else:
            print(f"Ошибка {response.status_code}: {response.text}")
            return {"error": response.status_code, "message": response.text}

    def get_map(self, cluster: str) -> list:
        """
        Получение пиров, которые сидят в трайбе
        """
        cluster_id = self.clust_keys.get(cluster)
        if cluster_id is None: return
        request = f'/v1/clusters/{cluster_id}/map'
        params = {'occupied': True, 'limit': 140}
        j = self.get('%s%s' % (self.url, request), params=params)
        return j['clusterMap']

    def get_tribe(self, login: str) -> str:
        """
        Получение названия трайба
        """
        request = f'/v1/participants/{login}/coalition'
        r = self.get('%s%s' % (self.url, request))
        return r['name']

    def is_token_expired(self) -> bool:
        """
        Проверка на истек ли срок токена
        """
        return time.time() > self.expires_in
    
    def close(self) -> None:
        """
        Закрытие сессии
        """
        if hasattr(self, 'session'):
            self.session.close()
            print("Сессия закрыта")

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Деструктор с закрытием сессии
        """
        self.close()