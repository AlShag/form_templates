# FastAPI form templates app 


## Stack:

- Python
- FastAPI
- MongoDB
- Docker

## Dependencies

- [docker](https://www.docker.com/)

## Installation

Using [Docker](https://docker.com):

```bash
# build
docker compose pull
docker compose build --parallel

# start (will run on http://localhost:8000)
docker compose up -d

# stop
docker compose down -t 0

# running tests
docker compose exec web pytest
```
