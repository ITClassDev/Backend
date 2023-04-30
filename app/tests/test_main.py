import requests as api

url = "http://localhost:8080"
def pth(endpoint): return f"{url}{endpoint}"

def test_main_api_ver():
    assert api.get(pth("/")).json()["api_ver"] == "0.0.2"

class JWT_Token:
    def __init__(self, token):
        self.token = token

    def correct(self):
        assert len(self.token.split(".")) == 3

token = JWT_Token("")

class TestAuth:
    def test_login(self):
        token.token = api.post(pth("/auth/login"), json={"email": "ret7020@gmail.com", "password": "12345"}).json()["accessToken"]
        token.correct()

    def test_auth_me(self):
        user = api.get(pth("/auth/me"), headers={"Authorization": f"Bearer {token.token}"}).json()["user"]
        assert user["id"] == 1
        assert user["firstName"] == "Stephan" 
        assert user["lastName"] == "Zhdanov"
    
    def test_bad_auth(self):
        assert api.post(pth("/auth/login"), json={"email": "ret7020@gmail.com", "password": "12345wwwwww"}).status_code == 401

    def test_login_validation(self):
        assert api.post(pth("/auth/login"), json={"em": "asdsdf", "passwo": "123"}).status_code == 422

class TestUser:
    def test_user_1(self):
        user = api.get(pth("/users/1")).json()
        assert user["firstName"] == "Stephan"
        assert user["lastName"] == "Zhdanov"
        assert user["middleName"] == "Alexeevitch"
        assert user["userTelegram"] == "Rtyrdv"
        assert user["userGithub"] == "ret7020"

