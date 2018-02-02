# docker-django-bank-management

Demonstration of a Django application that acts as a bank management solution.

## Features

* Requirements file
 
  - Django                 [x]

  - PostgresSQL libraries  [x]

* Create Django project [x]

* Create Django app banking [x]

  - register app in settings [x]

* Models []

  - Userdata    [x]

  - Tests       [x]

    a)  String representation [x]

* Admin         []

  - basic admin [x]

  - authentication []

    a) Google enabled authentication []

  - CRUD        [] 

  - Permissions []

     a) show only record belonging to admin creator []

     b) only admin creator can edit userdata record []

* Deployment    []

 - Docker       []

 - Test task    []
 


## Usage

Download the repository:
```
$ git clone https://github.com/gnud/docker-django-bank-management.git
```

Init project:
```
$ cd 'docker-django-bank-management'
$ virtualenv -p /usr/bin/python3 venv
$ source venv/bin/activate
$ pip install -r app/requirements.txt
```

Create Django project:
```
$ django-admin startproject bank
```

Setup database:
```
$ POSTGRES_PORT_5432_TCP_ADDR=localhost
$ POSTGRES_PORT_5432_TCP_PORT=5432
$ POSTGRES_DB_NAME=bankapp
$ PGUSER=django_usr
$ PGPASSWORD=django
$ sudo -u $PGUSER psql -c "CREATE DATABASE $POSTGRES_DB_NAME"
$ python manage.py makemigrations
$ python manage.py migrate
```

Create Django app:
```
$ cd bank
$ django-admin startapp banking
```

Test Django app:
```
$ python manage.py test banking
```

Launch:
```
$ python manage.py runserver
```

**Now your django app is available at [link](http://localhost:8000/), but it's optional for development**

Create a super user
```
$ python manage createsuperuser
```