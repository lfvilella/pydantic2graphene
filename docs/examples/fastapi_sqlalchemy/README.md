# FastAPI + SQLAlchemy + REST + GraphQL

This is an example of using the one schema to generate REST API and GraphQL endpoints and SQLAlchemy as database.


## Running locally

    $ docker run --rm -it -v $(pwd):/app -w /app -p 8000:8000 python:3.8 /bin/bash -c "pip install -r requirements.txt && uvicorn api:app --reload --host 0.0.0.0"
