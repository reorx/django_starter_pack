# Django Starter Pack

A collection of power packs to boost and enhance Django development, including:
- Project hierarchy
- Best practices
- Code snippets
- Utility functions


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
