# Description
This is the backend server for the physics tutoring portal. It interfaces between the PostgreSQL DB and the frontend server through a REST API.
Please read the following instructions carefully.

### Running Locally
1. Clone repository
2. Get .env files: one file goes in server and one goes in client
2. Install requirements.txt
```
$ pip install -r requirements.txt
```
3. Run the following command:
```
$ flask run
```
4. If that does not work try this:
```
$ gunicorn app:app
```
5. The server should be running

### Setting Up Local DB
1. Install requirements.txt (if you have not done so already)
```
$ pip install -r requirements.txt
```
2. Make sure that you have the [Postgres Application](https://www.postgresql.org/download/) *installed* and *running* on your computer.
3. Create a new database through terminal.
```
$ psql
# create DATABASE tutor_local;
CREATE DATABASE
# \q
```
This should create a new database that you can see in your Postgress Application called *tutor_local*.
4. Create a .env file in /server/ folder.

5. Run the following command in terminal:
```
$ export LOCAL_DATABASE_URL="postgresql://postgres:postgress@localhost/tutor_local"
```
6. Then add the following to the .env file.
```
LOCAL_DATABASE_URL=postgresql://postgres:postgress@localhost/tutor_local
```
