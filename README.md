# restaurant-booking-django
Complete end to end solution to restaurant booking built in Django Python

### Create virtual environment using PIP

    python3 -m venv .venv

### Active virtual environment(run any 1 command for active virtual environment)

    . .venv/bin/activate
    // or
    source .venv/bin/activate

### Install project requirement package 

    pip install -r requirements.txt

### Copy and setup .env file

    cp .env.example .env

### Run migration

    python manage.py migrate

### Create superuser for admin panel

    python manage.py createsuperuser

### Start server

    python manage.py runserver