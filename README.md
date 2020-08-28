# Learnpack API

This is the API for the Learnpack project, build using Python 3.8 and the Django Rest Framework.


## Installation
 
Before you start installing the project make sure you have the following installed:
- Pyenv 
- Python 3.8 (using pyenv is recommended)
- Postgree database

### 1) Create the .env file

We need `.env` file that will contain the sensitive variables like 3rd party API Keys, etc.
Duplicate the `.env.example` file and rename the copy as `.env`.  
Change the variables values to your convenience, for example the `DATABASE_URL` you have the connection string to your local database.

### 2) Install the python dependencies packages:

```
$ pipenv install
```

### 3) Running the migrations

```
$ pipenv run migrate
```

P.D: Remember that every time you make a change on your models.py you will have to make the migrations again using `$ pipenv run migrate`

### 4) Run the project

```
$ pipenv run start
```



2. cuando me intento logguear debería pasar email y password

4. si me logueo exitosamente, debería crearse un token

5. si intento cambiar mi password con un token ya expirado, debería dar error

6. si intento cambiar mi email con un token ya expirado, debería dar error 

7. implementar token temporal



