# API docs
[🇬🇧 English](/README.MD) [🇷🇺 Russian](/README.RU.MD)
## Table of contents
1. [ General ](#general) 
2. [ Handling requests ](#req_handling) 
3. [ Deployment ](#deployment) 
4. [ Testing all API ](#tests)


<a name="general"></a>
## General
<p>This is a repository with a ShTP backend. To demonstrate and interact with the API, you can use swagger by building the repository locally (/docs).</p> 
Tech-Stack
1. FastAPI + ASGI, so <b>fully async app</b>
2. Postgresql
3. sqlalchemy(async driver) for ORM
4. Alembic
5. Pydantic
6. Protobuf(Proto3)
7. jose - JWT Auth
8. Self-written API test system

<a name="req_handling"></a>
## How we Handle HTTP Requests
<p>Our API supports 2 types of data serialization: JSON(we use in our React client) and ProtocolBuffer(we use in our Java Android client).<p>
<p>The use of protocol buffers can significantly speed up the work of a mobile application due to efficient binary serialization. And the main difficulty in implementing the buffer protocol is the beauty of the architecture of the final application.</p>
<p></p>

<a name="tests"></a>
## Why self-written tests?!?!?!
<p>Why did we invent the wheel and write a system for api test from scratch?<p>
<p>The main problem is support for protobuffers. We don't use them in the context of grpc, we use them as a separate tool for serializing packages. It makes no sense to get into the code of ready-made autotests - it is very long and inconvenient. It's faster to write your own test system and not fool around.</p>

