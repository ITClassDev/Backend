# API docs
[🇬🇧 English](/README.MD) [🇷🇺 Russian](/README.RU.MD)
## Table of contents
1. [ General ](#general) 
2. [ Handling requests ](#req_handling) 
3. [ Tasks organization ](#tasks_organization) 
4. [ OAuth scheme ](#oauth_scheme)
5. [ Deployment ](#deployment) 
6. [ Testing all API ](#tests)


<a name="general"></a>
## General
<p>This is a repository with a ShTP backend. To demonstrate and interact with the API, you can use swagger by building the repository locally (/docs).</p> 
<p>
<img src="https://raw.githubusercontent.com/ITClassDev/Backend/master/docs/images/swagger_openapi.png">
</p>
Tech-Stack

1. FastAPI + ASGI, so <b>fully async app</b>
2. Postgresql
3. sqlalchemy(async driver) for ORM
4. Alembic
5. Pydantic
6. Protobuf(Proto3)
7. jose - JWT Auth
8. Self-written API test system(to support protobuf)
9. Docker + Docker compose
10. Pipenv

<a name="req_handling"></a>
## How we Handle HTTP Requests
<p>Our API supports 2 types of data serialization: JSON(we use in our React client) and ProtocolBuffer(we use in our Java Android client).<p>
<p>The use of protocol buffers can significantly speed up the work of a mobile application due to efficient binary serialization. And the main difficulty in implementing the buffer protocol is the beauty of the architecture of the final application.</p>
<p>So, we have a routing that accepts an input as a pydantic object or a json, it is convenient to work with it, there is no need to worry about parsing inputs from the request. Routing returns a pythonic dictionary or also a pydantic object, which in our case is the same. In our project, everything is simple - there is a wrapper above the usual json routings, which converts the received input from the protobuffers into the one necessary for the endpoint and similarly works on the result of the endpoint, converting it into a protobuffer. More detailed diagram in the image below.</p>
<p>
<img src="https://raw.githubusercontent.com/ITClassDev/Backend/master/docs/images/req_flow.png">
</p>

<a name="tasks_organization"></a>
## Tasks_organization (backend level)
<p>Look at image</p>
<p>
<img src="https://raw.githubusercontent.com/ITClassDev/Backend/master/docs/images/tasks_organization.png">
</p>

<a name="oauth_scheme"></a>
## OAuth scheme
<p>I know, this is not a classic OAuth. It is low privileged shit, but it works and it is secure by design! So, shut up and use it!</p>
<p>
<img src="https://raw.githubusercontent.com/ITClassDev/Backend/master/docs/images/oauth.png">
</p>

<a name="deployment"></a>
## Deployment
<p>First of all, I want to say, that backend tested only on Linux system, and I think it will be difficult to run it on Windows (for example docker-compose with postgresql).</p>
<p>We will build full docker-compose with all backend, to run it with one command, but it will be later, so for now, we support only native deployment.</p>

### Steps
Install docker and docker-compose in your system. Arch example.
```
sudo pacman -S docker docker-compose  # install
sudo systemctl start docker.service   # run service
```
In root directory of Backend, execute command to run docker compose with postgresql. First run will download extra dependencies. You can change postgres version, database name, database auth data in `docker-compose.dev.yaml`.
```
sudo docker-compose -f docker-compose.dev.yaml up
```
You can send it in background, or open another shell. But don't stop it. </br>
Then, we need to get this docker instance ip. </br>
The easiest method, to do it is: </br>
Get Container ID of our docker instance(CID):
```
docker ps
```
And then, execute this command (replacing CID with your container id):
```
docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' CID
```
After that you will get ip of your postgresql, it is local ip and works only on your pc. </br>
Than in `.env` file(in root of Backend project) you can change postgresql access data: </br>
```
ITC_DATABASE_URL = postgresql://{USERNAME}:{PASSWORD}@{CONTAINER IP}:{PORT}/{DB_NAME}
```
```
# params
USERNAME = default is root
PASSWORD = default is root
CONTAINER IP - your container id, from previous step
PORT = default is 5432
DB_NAME = default itc_system
```
So, another variables, that you can change in `.env` file:
```
ITC_SERV_PORT = http port of your backend
ITC_SERV_HOST = http host, listen from - 0.0.0.0 - to listen all hosts
ITC_SECRET_KEY = CHANGE ON PRODACTION, this is sault for jwt hashes
ITC_ACCESS_TOKEN_EXPIRE_MINUTES = jwt tokens life time in minutes, 1440 minutes = 24 hours
ITC_USERS_STORAGE = PATH to file storage directory; user uploads here
ITC_API_VER = version of your project
```
Now, we have to jump into virtual enviroment. In this project we use pipenv. Install it, if you don't have it yet. (Arch example)
'''
sudo pacman -S python-pipenv # or via pip - pip install pipenv
'''
Than, activate shell, via (do it in root directory of backend):
```
pipenv shell
```
Install all dependencies (one off methods)
```
pipenv install Pipfile
```
Now we have to import database struct to our database. We use alembic, so we can try, to use migrations
```
alembic upgrade head
```
After all done, try to run backend, via
```
python3 main.py
```
It will run! With default config, it will be `localhost:8080`
<a name="tests"></a>
## Why self-written tests?!?!?!
<p>Why did we invent the wheel and write a system for api test from scratch?<p>
<p>The main problem is support for protobuf. We don't use them in the context of grpc, we use them as a separate tool for serializing packages. It makes no sense to get into the code of ready-made autotests - it is very long and inconvenient. It's faster to write your own test system and not fool around.</p>


## Extra
### User roles:
0 - Base student
1 - Teacher - Now have access to all features, but we will fix it later
2 - Super Admin - Have access to all features


## Dev notes (remove later)
// Notifications types
// 0 - achievement moderated true
Ваше достижение {name} прошло модерацию! Начислено {points} баллов 
points; achievemnt name
// 1 - achievement moderated rejected
Ваше достижение {name} отклонено!
name
// 2 - new local(school) event added
Добавлено новое школьное событие - {name}
event name
// 3 - new medal
Вы получили новую {medal type} медаль!
medal type