import requests

class User:
    def __init__(self, host="http://localhost:8080"):
        self.authed = False
        self.id = None
        self.access_token = None
        self.host = host

    def auth(self, email, password):
        if not self.authed:
            server_resp = requests.post(f"{self.host}/auth/login", json={"email": email, "password": password})
            if server_resp.status_code == 200: # Successful auth
                self.access_token = server_resp.json()['access_token']
                self.authed = True

    def test_protected_endpoint(self, endpoint="users/test_auth"):
        if self.authed:
            data = requests.get(f"{self.host}/{endpoint}", headers={"Authorization": f"Bearer {self.access_token}"})
            if data.status_code == 200:
                self.id = data.json()['user_id']
                self.f_name = data.json()['user_fname']
                return True
        return False

if __name__ == "__main__":
    client = User()
    client.auth("ret7020@gmail.com", "12345")
    res = client.test_protected_endpoint()
    if res:
        print(client.id, "-", client.f_name)
    else:
        print("Error")