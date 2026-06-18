# Backend
backend service


api flow tests:
###
```shell
uv run behave
```

___
## run db migrations

### create alembic migration
```shell
uv run alembic revision --autogenerate
```
### apply them to local db
```shell
uv run alembic upgrade head
```
### (optional) get the sql for it
```shell
uv run alembic upgrade head --sql
```
### verify it worked(heck if database is in sync with models)
```shell
uv run alembic check
```

___
## run pre-commit

### check if it's installed
```shell
pre-commit --version
```
### install pre-commit
```shell
pre-commit install
```
### apply pre-commit autoupdate
```shell
pre-commit autoupdate
```
### apply pre-commit for all files
```shell
pre-commit run --all-files
```
