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
        Get token (or refresh, if has refresh_token)
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
            print(f"Error {response.status_code}: {response.text}")
            return {"error": response.status_code, "message": response.text}

    def get_map(self, cluster: str) -> list:
        """
        Get peers from cluster
        """
        cluster_id = self.clust_keys.get(cluster)
        if cluster_id is None: return
        request = f'/v1/clusters/{cluster_id}/map'
        params = {'occupied': True, 'limit': 140}
        j = self.get('%s%s' % (self.url, request), params=params)
        return j['clusterMap']

    def get_tribe(self, login: str) -> str:
        """
        Get tribe name
        """
        request = f'/v1/participants/{login}/coalition'
        r = self.get('%s%s' % (self.url, request))
        return r['name']
    
    def get_tribe_with_retry(self, login: str, retry: int = 3):
        """
        Get tribe name with retry
        """
        for attempt in range(retry):
            try:
                tribe = self.get_tribe(login)
                return tribe
            except Exception as e:
                if "rate limit" in str(e).lower() or getattr(e, 'status', 0) == 429:
                    wait = 2 ** attempt
                    time.sleep(wait)
                else:
                    raise
        return None


    def is_token_expired(self) -> bool:
        """
        Check if token expired
        """
        return time.time() > self.expires_in
    
    def close(self) -> None:
        """
        Close session
        """
        if hasattr(self, 'session'):
            self.session.close()
            print("Session close")

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        close session in destructor
        """
        self.close()