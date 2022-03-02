# Simple Video Manager

## Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)

## About <a name = "about"></a>

This repo is a simple video manager with Django3.2 and DRF, which JWT authentication requires for all video and user endpoints unless the creation and the JWT token getter.

**_This library has been tested with GitHub Workflows._**

## Getting Started <a name = "getting_started"></a>

First convert `.env.example` to `.env` then if you want to change the values (by default, it works fine), be sure you installed Docker and docker-compose on your machine, then for the first time use:

`docker-compose up --build`

After the first time, you can remove the `build` switch. like: `docker-compose up`

### Prerequisites

- Docker
- docker-compose

### Tech Stack

- Python
- Django3.2
- Django REST framework
- Docker
- Docker-compose
- PostgreSQL
- Redis
- Gunicorn
- JWT Authentication
  
## Usage <a name = "usage"></a>

By default, it listens on port 8000, so for calling the endpoints, you have to call `127.0.0.1:8000/api/<endpoint>`:
It provides eleven endpoints. First, you must create a user, obtain a JWT access token, and refresh the token with that username and password.

- /create_user `POST` with user parameters in the body of your request. e.g.:
`{
    "username": "test",
    "email":"test@test.com",
    "bio": "test",
    "password": "sUper_Secret"
}`
This endpoint returns all user data, including the id, unless the password.

- /token `POST` call this with the username and password for obtaining JWTs, like: `{"username": "test", "password": "sUper_Secret"}`. This endpoint returns JWT tokens (access and refresh).

- /token/refresh `POST` call this with a JSON in request body including of refresh token, then it returns new tokens.

- /token/verify `POST` with a token in your json request body for verifying the token. like: `{"token":<your_token>}`

**_Then you have to pass the access token for all requests below to get the response. 
<br>In header of your request add `{"Authorization": "JWT <accsess_token>"}`._**
  
- /videos `GET` returns all videos (id and names)
  
- /upload `POST` with multipart format and the request must consist of name and a video, like: `{"name":"foo", "video": <your_target_file>}` then it returns all video data including id and link.
  
- /video/<video_id> `GET` returns all data from that specific video
  
- /video/<video_id> `PATCH` you can update the target video attribute/s. For instance, you can only update the file's name or both. You have to send the request in multipart format, including your target fields.

- /user/<username> `PATCH` you can update the user data, all fields or some of them or one of them.
  
- /user/<username> `DELETE` removes the target user.

- /user/<username> `GET` returns all user data except the password.
