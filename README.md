# Django Starter Pack

A collection of power packs to boost and enhance Django development, including:
- Project hierarchy
- Best practices
- Code snippets
- Utility functions


## How to use

1. clone the repo
2. copy to destination:

  ```
  rsync -avr --exclude venv --exclude test --exclude .git --exclude __pycache__ django_starter_pack/ $destination/
  ```
3. move `starter_app` to new package name
4. replace all `starter_app` occurrences with new package name


## Initilization

1. migrate database and create superuser

  ```
  python manage.py migrate
  python manage.py createsuperuser
  ```
2. run server

  ```
  python manage.py runserver
  ```
3. open http://localhost:8000/admin/ and login with superuser
4. create a new Org, then create a new user to join the org
5. test login API with the new user

  ```
  ./curlapi.sh /auth/login -X POST -d '{"username":"youruser","password":"yourpass"}'
  ```
6. test other APIs

  ```
  ./curlapi.sh /org/list
  ./curlapi.sh /group/list
  ./curlapi.sh /user/list
  ```
