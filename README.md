# docker-django-bank-management

Demonstration of a Django application that acts as a bank management solution.

## Features

* Requirements file
 
  - Django                 [x]

  - PostgresSQL libraries  [x]

* Create Django project [x]

* Create Django app banking [x]

  - register app in settings [x]

* Models [x]

  - Userdata    [x]

  - Tests       [x]

    a)  String representation [x]

* Admin         [x]

  - basic admin [x]

  - authentication [x]

    a) Google enabled authentication [x]

  - CRUD        [x]

  - Permissions [x]

     a) show only record belonging to admin creator [x]

     b) only admin creator can edit userdata record [x]

* Deployment    [x]

 - Docker       [x]

 - Test task    [x]


## Fixes
- no validation of IBAN (requested features)                        []
- a lot of unnecessary boilerplate code (eg unused requirements,
  template content)                                                 [x]
- Change of an object instance in a signal (create_user_profile).
This should take place in the model's save () method                []
- UserdataAdminTest is incomplete. The implemented test case makes
  little sense                                                      []


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
$ pip install -r bank/requirements.txt
```

Create Django project:
```
$ django-admin startproject bank
```

Setup database:
```
$ POSTGRES_PORT_5432_TCP_ADDR=localhost
$ POSTGRES_PORT_5432_TCP_PORT=5432
$ POSTGRES_DB_NAME=bank
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

Docker:

## Initial Setup
```
$ python manage collectstatic
$ sudo docker-compose build --force-rm --no-cache
$ # sudo docker-compose up postgres # To troubleshoot
$ sudo docker-compose up -d postgres
$ sudo docker-compose run bank setup_db # see deployment/docker-entrypoint.sh for more info
$ sudo docker-compose up web # this will launch a production version
```

## Launch

**Now your django app is available at [link](http://localhost/)**

## Common tasks
After each library install run

```
$ python manage collectstatic
$ sudo docker-compose build
$ sudo docker stop $(sudo docker ps -aq)
$ sudo docker-compose up web # this will launch a production version
```

## Run Docker Tests

```
sudo docker-compose run bank manage test
```

Workflow for publishing changes

```
$ sudo docker-compose build
$ sudo docker stop $(sudo docker ps -aq)
$ sudo docker-compose up web # this will launch a production version
```

## TROUBLESHOOT
Exec bash in any container

Troubleshoot the nginx server
```
$ sudo docker exec -it dockerdjangobankmanagement_web_1 sh
$ cd /var/log/nginx/
$ tail -f *
```


Troubleshoot the django server
```
$ sudo docker exec -it dockerdjangobankmanagement_bank_1 sh
$ tail -f *.log
```


Full refresh from scratch
**WARNING**: Make sure you don't have any personal containers!
Doing so will remove everything.

```
$ sudo docker stop $(sudo docker ps -aq)
$ sudo docker rm $(sudo docker ps -aq)
$ sudo docker-compose build --force-rm --no-cache
```
