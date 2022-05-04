# OC_Projet_12
Développez une architecture back-end sécurisée en utilisant Django ORM

## Set up the project
This project runs in python 3

Make a copy of this project on your hard drive <br>
`git clone https://github.com/friquette/OC_Projet_12.git`

Go in the root project and create a virtual environment <br>
`cd OC_Projet_12` <br>
`python -m venv env`

Activate your virtual environment <br>
- On Windows `env\Scripts\activate.bat`
- On Mac OS/Linux `source env/bin/activate`

Go in the project folder
`cd epic_events`

Install the packages <br>
`pip install -r requirements.txt`

## Set up your postgresql database
Create a database with postgresql, and don't forget to set it
correctly in the settings of django like this<br>
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '<database_name>',
        'USER': '<username>',
        'PASSWORD': '<database_password>',
        'HOST': '<host>',
        'PORT': '<port>',
    }
}
```
If you're not familiar with the installation of the postgresql database, you
can follow this official tutorial: https://www.postgresqltutorial.com/postgresql-getting-started/install-postgresql/

## How to use it
For the first time you are using the application, migrate the tables in the database<br>
`python manage.py migrate`

And load the fixtures data in the database<br>
`python manage.py loaddata employees/fixtures/groups.json`

Run your server<br>
`python manage.py runserver` <br>

Before sending the application online, open the settings.py file in softdesk folder,
and change the `DEBUG = True` to `DEBUG = False`

To interrupt your server, simply hit `CTRL+C` in your command prompt.

## Admin part

To create an admin user, go to the root application folder and enter:
`python manage.py createsuperuser`
and follow the instructions.

To access the admin site page, go to
`localhost:8000/admin` in your web browser. Only admin users can access this
page.

## Documentation

To see the full document of the API, go to
`https://documenter.getpostman.com/view/14738930/UyxbppAz`
