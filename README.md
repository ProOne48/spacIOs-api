# spacIOs-api
Repository for the api of the SpacIOs app that would be the TFG of an student of the University of Granada (UGR)

## Description

This app will be focus in managing spaces in buildings as gyms, bars, restaurant,... In the app the user will be able to see the how much full a place is and when a person is in one place it should register like if he is in that place and logout of that place, obviously no with a normal login but with some QR or something similar.

## Counting capacity

The user will scan a QR code and from then until the token expire or the user scan it again it will be counted as it is in the space. 


# API

The API will be developed in Python with the framework Flask and it will be deployed in Heroku. The database will be PostgreSQL.

## Installation

### 1. Clone the project

```bash
git clone https://github.com/ProOne48/spacIOs-api.git
```

### 2. Install Python dependencies

```bash
./scripts/install_local.sh
```

### 3. Install PostgreSQL server

The API uses PostgreSQL 15.0 as database server within a Docker container. You can run it with the following command:

```shell
docker-compose -f ./docker/db.docker-compose.yml --env-file ./docker/db-local.env up -d
```

### 4. Setup the configuration

- Create a `.secrets.local.toml` file from `template.secrets.local.toml`
- Customize the environment vars in the `.secrets.local.toml` file.
- If you need to modify the db-local.env file be careful to change the `.secrets.local.toml` so the data match.

### 5. Run the API
To run the API in Linux use this command:

```shell
python3 server.py
```
