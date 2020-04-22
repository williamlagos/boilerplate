# Cloud boilerplate

Cloud boilerplate written with Python and Django, with continuous integration from GitHub to Heroku Platform with Heroku Postgres and Heroku Redis. A calculator sample was developed for testing the infrastructure. To basically run a copy on docker:

``
$ docker build . -t boilerplate
``

``
$ docker run -p 8000:8000 -d boilerplate
``

Or to run heroku production locally (with heroku deployed and logged in):

``
$ ./manage.py migrate
``

``
$ ./manage.py collectstatic --noinput
``

``
$ heroku local
``