# Emote Care API 

Written with [Django](https://www.djangoproject.com/) and [DRF](https://www.django-rest-framework.org/)

## Requirements to run this project using Docker

- docker (20.10.5+): To install docker visit https://docs.docker.com/get-docker/
- docker-compose (1.25.5+): To install docker-compose visit https://docs.docker.com/compose/install/


## Getting started

**To start project with Docker:**
 - install docker
 - install docker-compose
 - Clone the project  
 - Change directory to the project directory 
 - Run:
    ```bash
        docker-compose up
    ```
  - The application would be available at http://127.0.0.1:8000

**To start project without Docker using virtualenv:**
 - Change directory to the project directory     
 - create a virtualenv
 - activate the previously created virtualenv
 - Run:
    ```bash
        pip install -r <path_to_requirements.txt>
    ```
 - Change directory to the directory of ```manage.py``` file
 - Run to makemigrations: 
    ```bash
        python manage.py makemigrations
    ```
 - Run to migrate:
    ```bash
        python manage.py migrate
    ```
 - Run to runserver:
    ```bash
        python manage.py runserver
    ```
  - The application would be available at http://127.0.0.1:8000


## Project commands using docker

Start a new app:

```bash
docker-compose run --rm emote_api sh -c "python manage.py startapp {app_name}"
```

Create superuser:

```bash
docker-compose run --rm emote_api sh -c "python manage.py createsuperuser"
```

Makemigrations:

```bash
docker-compose run --rm emote_api sh -c "python manage.py wait_for_db && python manage.py makemigrations"
```

To migrate:

```bash
docker-compose run --rm emote_api sh -c "python manage.py wait_for_db && python manage.py migrate"
```

To makemigrations and migrate:

```bash
docker-compose run --rm emote_api sh -c "python manage.py wait_for_db && && python manage.py makemigrations && python manage.py migrate"
```

To run test suites:

```bash
docker-compose run --rm emote_api sh -c "python manage.py wait_for_db && python manage.py test"
```

To run test coverage:
```bash
docker-compose run --rm seedfi_underwriting_api sh -c "python manage.py wait_for_db && coverage run manage.py test && coverage report"
```

To check lint:

```bash
docker-compose run --rm emote_api sh -c "flake8"
```

To run tests and check lint:

```bash
docker-compose run --rm emote_api sh -c "python manage.py wait_for_db && python manage.py test && flake8"
```

To install new packages:

Add the package name to  ```requirement.txt``` file
then run 

```bash
docker-compose up --build
```

To tear down the all containers:

```bash
docker-compose down
```

isort:

```bash
docker-compose run --rm emote_api sh -c "isort ."
```

## API Documentation

API documentation for this project is available at: `v1/api_docs/`
API documentation schema for this project is available at: `v1/api/schema/`
