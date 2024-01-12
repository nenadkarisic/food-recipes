# VortexWest Assignment - Food Recipes

### Running the app via docker-compose

Before running the app via `docker-compose up` command, there are some steps that need to be taken:
* in the same folder where `docker-xompose.yaml` is located, create a `.env` file, based od the `.env.template` file provided in the same folder.
* Enter all the required information so that they can be set as environment variables, used for database connection, automated super-user creation, and user og PgAdmin UI interface for Postgres monitoring, etc.

For example, contents of `.env` file can be like this:

``` 
POSTGRES_DB=recipes
POSTGRES_USER=myuser
POSTGRES_PASSWORD=mypassword

DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_PASSWORD=adminpass
DJANGO_SUPERUSER_EMAIL="admin@admin.com"
DJANGO_SUPERUSER_FIRST_NAME=John
DJANGO_SUPERUSER_LAST_NAME=Doe

PGADMIN_DEFAULT_EMAIL=user@user.com
PGADMIN_DEFAULT_PASSWORD=password

DEBUG=True
DJANGO_SECRET_KEY="<random_generated_django_secret>"

HUNTER_API_KEY=<hunter_api_key>
CLEARBIT_API_KEY=<clearbit_api_key>
```
When you have created the `.env` file and populated these variables, you can run `docker-compose up` command, which 
will perform the following steps:
* pull the needed images
* build and run the containers for defined services
* instantiate the database
* perform necessary migrations
* create the superuser
* run the app on `0.0.0.0:8000`.