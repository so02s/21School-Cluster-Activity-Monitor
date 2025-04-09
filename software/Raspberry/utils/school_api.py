import time
import requests

class SchoolClient:
    def __init__(self, username: str, password: str):
        self.url = "https://edu-api.21-school.ru/services/21-school/api"
        self.auth_url = "https://auth.sberclass.ru/auth/realms/EduPowerKeycloak/protocol/openid-connect/token"
        self.client_id = 's21-open-api'
        self.username = username
        self.password = password
        self.token = None
        self.refresh_token = None
        self.expires_in = None
        self.clust_keys = {"at": 34715, "il": 34718, "mi": 34719,"oa": 34720}
        self.get_token()

    def get_token(self):
        auth_data = {
            "username": self.username,
            "password": self.password,
            "grant_type": "password",
            "client_id": self.client_id
        }
        response = requests.post(self.auth_url, data=auth_data)
        if response.status_code == 200:
            token_data = response.json()
            self.token = token_data["access_token"]
            self.refresh_token = token_data["refresh_token"]
            self.expires_in = token_data["expires_in"]
        else:
            raise Exception("Failed to get token")

    def refresh_token(self):
        refresh_data = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
            "client_id": self.client_id
        }
        response = requests.post(self.auth_url, data=refresh_data)
        if response.status_code == 200:
            token_data = response.json()
            self.token = token_data["access_token"]
            self.refresh_token = token_data["refresh_token"]
            self.expires_in = token_data["expires_in"]
        else:
            raise Exception("Failed to refresh token")

    def get(self, url, params=None):
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 401:
            self.refresh_token()
            return self.get(url)
        else:
            return response.json()

    def get_map(self, cluster: str) -> list:
        cluster_id = self.clust_keys.get(cluster)
        if cluster_id is None: return
        request = f'/v1/clusters/{cluster_id}/map'
        params = {'occupied': True, 'limit': 140}
        j = self.get('%s%s' % (self.url, request), params=params)
        return j['clusterMap']

    def get_tribe(self, login: str) -> str:
        request = f'/v1/participants/{login}/coalition'
        r = self.get('%s%s' % (self.url, request))
        return r['name']

    def is_token_expired(self):
        return time.time() > self.expires_in