# Family budget

Family budget is an application that allows to create budgets and managing expanses.

## Installation

Use the docker-compose to run the app. Docker-compose includes containers with postgres database and django app instance.

```bash
docker-compose up
```

## Technologies
Application is written with django framework with graphQL API. Authentication is created with `django-graphql-auth` package, that allows to fully handle users actions (i.e. register, verify, login, change password etc.). 
## Usage
API can be tested through endpoint on `http://localhost:8000/graphql` or any other software, that allows to send  HTTP requests to address above.
## Tests
There were created basic tests with fixtures for API and models' properties. To run tests, type `pytest` in main project directory.