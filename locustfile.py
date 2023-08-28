from locust import HttpUser, between, task
import logging

EMAIL = "" 
PASSWORD = ""

class WebsiteUser(HttpUser):
    wait_time = between(5, 10)
    def on_start(self):
        token = self.client.post('/api/v1/auth/login', json={'email': EMAIL, 'password': PASSWORD})
        self.client.headers = {'Authorization': f'Bearer: {token.json()["accessToken"]}'}
    
    @task
    def token_gen(self):
        self.client.post('/api/v1/auth/login', json={'email': EMAIL, 'password': PASSWORD})

    @task
    def index(self):
        self.client.get("/")

    @task
    def index(self):
        self.client.get("/api/v1/auth/me")
        
    @task
    def profile(self):
       self.client.get("/u/ret7020")
    
    @task
    def profile_2(self):
        self.client.get("/u/admin")

    @task
    def docs(self):
       self.client.get("/docs")
    
    @task
    def leaderboard(self):
        self.client.get("/leaderboard")

    @task
    def notifications(self):
        self.client.get("/notifications")

    @task
    def events(self):
        self.client.get("/events")

    @task
    def settings(self):
        self.client.get("/settings")