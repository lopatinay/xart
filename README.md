# xart test api

# Start 
## via docker-compose

First of all run database
```bash
docker-compose up -d postgres
```

Then migrations
```bash
docker-compose up migration
```

Then you can run all services
```bash
docker-compose up -d
```

## localy
Run database
```bash
docker-compose up -d postgres
```

Migrate
```bash
make migrate
```

Create test users
```bash
python manage.py init_users
```

4 users will be created with QA role and one with ADMIN. They all have same password `password`
```
admin@xart.com"
kevin@xart.com
qa2@xart.com
qa3@xart.com
qa4@xart.com
```

Populate assets
```bash
python manage.py populate_data
```

# Runserver

```shell
python manage.py runserver
```

API base path: `http://0.0.0.0:9000/api/v1`

API docs: `http://0.0.0.0:9000/docs` or `http://0.0.0.0:9000/redoc`


# Play
## via postman
You can find a postman collection `postman_collection.json`.

Setup 1 global environment (and activate it on top left dropdown):
```
api=http://0.0.0.0:9000/api/v1
```

Auth endpoint has test, that test automatically set jwt token. Check `Trax test` collection `Authorization`
should have type Bearer token and Token `{{access_token}}` 

### 1. login
Application uses JWT authentication

```bash
POST http://0.0.0.0:9000/api/v1/auth/token
```

body:
```json
{
    "email": "kevin@xart.com",
    "password": "password"
}
```

response:
```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NywiZW1haWwiOiJrZXZpbkB4YXJ0LmNvbSIsInJvbGUiOiJRQSIsImV4cCI6MTY3ODE0MDQ0MX0.zO1DWzwNXEIzPqsy1SqOmy3tYjMFy8o06037xaPzXKE",
    "expired_id": 86399,
    "token_type": "bearer"
}
```

### 2. Create challenge
Challenge will be created for current user (authorized via jwt token)
```bash
POST http://0.0.0.0:9000/api/v1/challenges
```

### 3. Retrieve 100 voting in progress
```bash
GET http://0.0.0.0:9000/api/v1/voting
```

### 4. Retrieve next voting
```bash
GET http://0.0.0.0:9000/api/v1/voting/next
```

### 5. Solve challenge
```bash
POST http://0.0.0.0:9000/api/v1/challenges
```
body
```json
{
    "product_id": 4,
    "snapshot_id": 1854,
    "decision": true
}
```


# Tests

Run coverage
```shell
make coverage
```

# Migrations

__Autogenerate changeset__  
When you change or add a new model, this command will automatically generate the changeset
```shell
alembic revision --autogenerate -m "init"
```

__Manually changeset__  
In this case, an empty changeset will be generated, which you need to fill in yourself.
```shell
alembic revision -m "Added account table"
```

__Migrate__  
Apply changeset to Database
```shell
make migrate
```

__Rollback__  
On every call will be rolled back 1 changeset
```shell
make rollback
```
