INSTALLATION
------------

Please make sure the release file is unpacked under a Web-accessible
directory. You shall see the following files and directories:

      klinika/             framework source files
      works/               works
      Pipfile/             requirement checker
      Pipfile.lock/        requirement checker
      README               this file


REQUIREMENTS
------------

Python (3.7, 3.8, 3.9)
Django (3.0, 3.1)
We highly recommend and only officially support the latest patch release of each Python and Django series.

QUICK START
-----------

Klinika comes with a command line tool called "python3"

On command line, type in the following commands:

        $ cd Klinika                (Linux)
        cd Klinika                  (Windows)


Installation
-----------


        Install using pipenv...
        virtualenv venv
        source venv/bin/activate
        pipenv run



Example
-----------

Let's take a look at a quick example of using Klinika

Startup up a project like so...


        pipenv run python3 manage.py migrate
        pipenv run python3 manage.py createsuperuser
        pipenv run python3 manage.py runserver

Deploy
-----------



        sudo docker-compose build
        sudo docker-compose up -d
        sudo docker-compose exec web pipenv run python3 manage.py makemigratons
        sudo docker-compose exec web pipenv run python3 manage.py migrate
        sudo docker-compose exec web pipenv run python3 manage.py collecstatic
        sudo docker-compose exec web pipenv run python3 manage.py createsuperuser
