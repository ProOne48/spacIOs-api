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


## Alembic guide for database migrations

### Upgrading & downgrading your database

The upgrade database command is:

```shell
alembic upgrade <revision-number>
```

Where `<revision-number>` is the hexadecimal ID that you can find inside the revision file.

To upgrade to the latest version you can simply run:

```shell
alembic upgrade head
```

If for some reason you want to roll back to a previous version of the database, you can do it with:

```shell
alembic downgrade <revision-number>
```

To downgrade to the first revision run:

```shell
alembic downgrade base
```

### Creating a new database migration

Database revision files are stored in `./src/db/migrations/versions`. In order to create a new database migration you
should create a new migration file and fill the two `upgrade` & `downgrade` functions. To do so, follow these steps:

- Run the command:
  ```shell
  alembic revision -m "my revision description" --autogenerate
  ```
- A new file with the format `YYYYMMDD_HEXNUMBER_DESCRIPTION.py` will be created at `./src/db/migrations/versions/`.
  Open it.
- Review the `upgrade` function. The `autogenerate` param should already have created the instructions to apply. Check
  that everything is fine.
- Review the `downgrade` function. The `autogenerate` param should already have created the instructions to apply to
  roll back to the previous version. Check that everything is fine.
- If the `upgrade` & `downgrade` functions are empty then you probably forgot to add the model to
  the `./src/db/migrations/env.py` file.
- Test your migration with the console commands above.
