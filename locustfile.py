from locust import HttpUser, between, task

class WebsiteUser(HttpUser):
    wait_time = between(5, 10)
    def on_start(self):
        token = self.client.post('/api/auth/login/', json={'email': 'ret7020@gmail.com', 'password': '5322435Sz!'})
        self.client.headers = {'Authorization': f'Bearer: {token.json()["accessToken"]}'}
    
    @task
    def index(self):
        pass
        self.client.get("/")
        
    @task
    def profile(self):
       self.client.get("/profile?id=1")
    
    @task
    def profile_2(self):
        self.client.get("/profile?id=2")


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
    def settings(self):
        self.client.get("/settings")

    @task
    def challenge(self):
        self.client.get("/tasks/challenge")


