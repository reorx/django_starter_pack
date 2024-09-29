# pull official base image
FROM python:3.10

# set working directory
WORKDIR /app

# install system dependencies
# ADD dev/sources.list /etc/apt/
# RUN apt-get update
# for mysql
RUN apt-get -y install gcc default-libmysqlclient-dev

# install python dependencies
RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/
RUN pip config set install.trusted-host mirrors.aliyun.com
ADD requirements.txt .
RUN pip install -r requirements.txt

# add app
ADD *.py .
ADD starter_app ./starter_app
ADD uwsgi.ini .

# collect static files
RUN python manage.py collectstatic

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_ROOT_USER_ACTION=ignore PYTHONPATH=.

CMD ["uwsgi", "uwsgi.ini"]
