# FastAPI with REST and GraphQL

This is an example of using the one schema to generate REST API and GraphQL endpoints.


## Running locally

    $ docker run --rm -it -v $(pwd):/app -w /app -p 8000:8000 python:3.8 /bin/bash -c "pip install -r requirements.txt && uvicorn api:app --reload --host 0.0.0.0"

- Rest API: http://localhost:8000/docs
- GraphQL: http://localhost:8000/graphql

## GraphQL playground

-  http://localhost:8000/graphql

### Filter Items

![GraphQL filter gif](../../images/examples/fastapi_graphql_and_rest/graphql_filter.gif?raw=true)

![GraphQL filter](../../images/examples/fastapi_graphql_and_rest/graphql_filter.png?raw=true)

### Create Item

![GraphQL create gif](../../images/examples/fastapi_graphql_and_rest/graphql_mutation.gif?raw=true)

![GraphQL create](../../images/examples/fastapi_graphql_and_rest/graphql_mutation.png?raw=true)


## FastAPI playground

-  http://localhost:8000/docs

### Filter Items

![REST filter gif](../../images/examples/fastapi_graphql_and_rest/rest_filter.gif?raw=true)

### Create Item

![REST create gif](../../images/examples/fastapi_graphql_and_rest/rest_mutation.gif?raw=true)


### Overview

![REST example](../../images/examples/fastapi_graphql_and_rest/rest.png?raw=true)
