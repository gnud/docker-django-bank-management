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

  - Tests       []

* Admin         []

  - basic admin []

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