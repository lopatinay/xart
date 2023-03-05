# xart test api

# Runserver

```python
python manage.py runserver
```

API base path: `http://0.0.0.0:9000/api/v1`

API docs: `http://0.0.0.0:9000/docs` or `http://0.0.0.0:9000/redoc`


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
