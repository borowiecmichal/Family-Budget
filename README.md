# Family budget

Family budget is an application that allows to create budgets, controlling incomes and expanses.

## Installation

Use the docker-compose to run the app. Docker-compose includes containers with postgres database and django app instance.

```bash
docker-compose up
```

## Technologies
Application is written with django framework with graphQL API. Authentication is created with `django-graphql-auth` package, that allows to fully handle users actions (i.e. register, verify, login, change password etc.).  
Filtering and pagination are implemented by using relay interface while creating GraphQL API.  
To use pagination, add arguments like `offset, before, after, first, last` to query that returns list of objects, according to [GraphQL Pagination Docs](https://graphql.org/learn/pagination/).  
Filtering was also partly created by using relay interface. There were also added some customized filters, by creating models' filtersets.
## Usage
API can be tested through endpoint on `http://localhost:8000/graphql` or any other software, that allows to send  HTTP requests to address above. On this address is also available full API documentation.
## Tests
There were created basic tests with fixtures for API and models' properties. To run tests, type `pytest` in main project directory.