# fake_service_demo
Just some demo project with service that fakes some tasks

# Run services on bare-metal
## Prepare environment
Setup your postgres database and redis service and make sure to create conf.yaml with you database settings and your redis settings.
Also you can specify api server settings like port.
Also you need to install pip requirements, you can do that by `pip3 install -r requirements.txt`

## Run tests

You can run tests from src folder using `python3 -m pytest tests`

## Run migrations
For running services you need to complete migrations, you can do that by:
`cd src && python3 -m app.migrations.cli apply`

## Run services
### Run api server
Execute `python3 -m run api`

### Run worker server
Execute `python3 -m run worker`/
Open http://0.0.0.0:4321/docs#/ in browser (Or whatever port and host you set in your con.yaml file)

# Run services using docker-compose
Run `docker-compose up` from root directory of the project. 


# Task 1
You can find answers on Task 1 questions in ANSWERS.md file